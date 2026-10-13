# Auth Headers, Cookies, Caching, Redirects, and CORS

## 1. Metadata and prerequisites

- Topic IDs: D01-T15, D01-T16, D01-T17, D01-T18, D01-T19, D01-T20
- Domain: 1, HTTP and Web Fundamentals
- Difficulty: Intermediate
- Prerequisites: D01-T07, D01-T08, D01-T09, D01-T11
- Learning objectives:
  - Describe `Authorization`, `WWW-Authenticate`, cookies, and sessions at the HTTP layer.
  - Explain `Cache-Control`, validators, and conditional requests.
  - Choose redirect status behavior and explain a CORS preflight.
- Related topic IDs: D03-T12, D03-T13, D03-T15, D07-T02, D07-T19, D07-T20, D09-T05
- Estimated complexity: high for a first pass
- Completion status: TECHNICALLY_REVIEWED
- Verification: RFC 9110, RFC 9111, and the Fetch CORS model reviewed 2026-10-13. No browser session was executed. Curl and Python sketches are unverified.

## 2. Introduction and fundamentals

### D01-T15 Authorization and WWW-Authenticate

`Authorization` carries credentials for this request.

```text
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.payload.sig
```

The scheme token is `Bearer`. Basic authentication is `Authorization: Basic <base64 user:password>`. Basic credentials are easy to leak into logs and have no scoped expiry. Use them only in narrow cases over TLS, if at all.

`WWW-Authenticate` is the challenge on a `401` response. It names the schemes the server will accept.

```text
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="api", error="invalid_token"
```

RFC 9110 keeps the reason phrase "Unauthorized" for unauthenticated requests. Do not return `403` for a missing token. `403` means the server understood the caller and refuses the action.

### D01-T16 Cookies and sessions

`Set-Cookie` asks the client to store a pair and send it later.

```text
Set-Cookie: session=abc123; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=3600
```

Later requests include `Cookie: session=abc123`.

A session is server-side state looked up by that id. The cookie is the key, not the session. If the cookie value is the user profile itself, the client can edit it unless you sign and encrypt it. Prefer a random id plus server state, or a specified token format.

| Flag | Effect |
| --- | --- |
| `HttpOnly` | Document scripts cannot read the cookie. |
| `Secure` | Browser sends it only on HTTPS. |
| `SameSite=Lax` or `Strict` | Limits cross-site sending. `None` requires `Secure`. |
| `Path` and `Domain` | Limit which requests include the cookie. A wide `Domain` includes more hosts than you intend. |

REST statelessness (D02-T04) means each request carries what the server needs to interpret it. A session row in a database is allowed. It is a different scaling choice than a self-contained token.

### D01-T17 Cache-Control, ETag, and Last-Modified

`Cache-Control` tells caches who may store a response and for how long (RFC 9111).

| Directive | Meaning |
| --- | --- |
| `max-age=60` | Fresh for 60 seconds. |
| `no-store` | Do not store it. |
| `no-cache` | Revalidate before reuse. It does not mean "do not store." |
| `private` | Shared caches must not store it. A private browser cache may. |
| `public` | Shared caches may store it. |
| `must-revalidate` | Do not use a stale copy without checking the origin. |

`ETag` is an opaque validator. A strong ETag changes when the representation bytes change. A weak ETag (`W/"abc"`) means semantic equivalence.

`Last-Modified` is coarser. Two updates in the same second can share a timestamp.

Authenticated order payloads should use `Cache-Control: private, no-store` unless a review says otherwise.

### D01-T18 Conditional requests

```text
GET /v1/products/7 HTTP/1.1
If-None-Match: "rev-9"
```

If the current ETag is still `"rev-9"`, respond `304 Not Modified` with no body. Authorization still runs. A `304` tells the caller that their validator matches; do not leak that fact to a caller who cannot read the resource.

`If-Match` protects writes. If the tag does not match, return `412` and do not write.

`If-Modified-Since` and `If-Unmodified-Since` are the time-based forms. Prefer ETags for records.

### D01-T19 Redirects

`Location` names the next URI.

| Code | Use | Next method |
| --- | --- | --- |
| 301 | Permanent move | Clients have historically changed POST to GET. Do not move a write API with 301. |
| 302 | Temporary move | Same historical method change. |
| 307 | Temporary move | Method and body stay. |
| 308 | Permanent move | Method and body stay. |

`303 See Other` asks the client to GET another URI after POST. That is the browser Post/Redirect/Get pattern. JSON APIs more often return `201` with `Location`.

### D01-T20 CORS and preflight

CORS is a browser rule for scripts. curl does not enforce it. A cross-origin JSON POST with `Authorization` is not a "simple" request, so the browser first sends OPTIONS.

```text
OPTIONS /v1/orders HTTP/1.1
Origin: https://shop.example
Access-Control-Request-Method: POST
Access-Control-Request-Headers: authorization,content-type
```

A useful response:

```text
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://shop.example
Access-Control-Allow-Methods: GET, POST
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Max-Age: 600
Vary: Origin
```

`Access-Control-Allow-Origin: *` cannot be combined with credentialed cookies. Reflecting any `Origin` while allowing credentials lets hostile sites call your cookie-authenticated API from a victim's browser.

CORS does not replace authorization. A stolen bearer token works from any HTTP client.

## 3. Internal workings

```mermaid
sequenceDiagram
  participant Client
  participant Origin
  Client->>Origin: GET /products/7
  Origin-->>Client: 200 ETag rev-9
  Client->>Origin: GET /products/7 If-None-Match rev-9
  Origin-->>Client: 304
```

```mermaid
sequenceDiagram
  participant Browser
  participant Origin
  Browser->>Origin: OPTIONS /v1/orders
  Origin-->>Browser: 204 allow POST
  Browser->>Origin: POST /v1/orders
  Origin-->>Browser: 201
```

If preflight fails, the POST never leaves the browser. Access logs show OPTIONS only. curl hides this bug because it sends POST directly.

## 4. Architecture diagrams

```mermaid
flowchart LR
  browser[Browser]
  api[API]
  store[SessionOrTokenKeyStore]
  browser -->|Cookie or Authorization| api
  api --> store
```

Stateless JWTs skip the store until you need revocation. Short lifetimes shrink that window. They do not remove the need for authorization on each object.

## 5. Code and implementation

Unverified.

```bash
curl -sS -D - -o NUL -H "Authorization: Bearer change-me" "https://api.example.com/v1/orders"
curl -sS -D - -H "If-None-Match: \"rev-9\"" "https://api.example.com/v1/products/7"
```

Public catalog item:

```text
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: public, max-age=60
ETag: "rev-9"

{"id":7,"name":"Pen"}
```

Private order:

```text
HTTP/1.1 200 OK
Cache-Control: private, no-store
Content-Type: application/json

{"id":100,"total":"12.00"}
```

```python
from starlette.responses import JSONResponse

def login_response() -> JSONResponse:
    response = JSONResponse({"ok": True})
    response.set_cookie(
        key="session",
        value="random-opaque-id",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600,
        path="/",
    )
    return response
```

`secure=True` cookies are not stored on plain `http://` origins. A local exception must not ship to production.

## 6. API contracts

| Concern | Contract |
| --- | --- |
| Auth | Bearer token except on public routes. Missing or bad token: `401` plus `WWW-Authenticate`. Known caller, forbidden action: `403`. |
| Cookies | Browser client only. Flags in the table above. |
| Public GET | `ETag` and a stated `max-age`. |
| Private GET | `private, no-store`. |
| Writes | Optional or required `If-Match`. Mismatch: `412` and no write. |
| Moves | Permanent API moves use `308`. |
| CORS | Explicit origin allow-list. |

## 7. Production considerations

Mandatory: cookie flags, `no-store` on private responses, authorization before `304`, CORS allow-list, no secrets in redirect URLs.

Optional: preflight `Max-Age`, HSTS after HTTPS is confirmed, ETags on public collections.

## 8. Comparison and tradeoffs

| Mechanism | Advantage | Cost | Use when |
| --- | --- | --- | --- |
| Bearer token | Non-browser clients | Theft if script can read storage; revocation is extra state | Mobile, partners, workers |
| Session cookie | `HttpOnly` | CSRF if SameSite is careless; session store | First-party browser app |
| `no-store` | Avoids leaked caches | No reuse | Profiles and orders |
| `no-cache` | Freshness with storage | A revalidation request | Large public documents |
| 308 | Keeps POST | Some very old clients | Permanent API move |
| 301 | Widely understood | May turn POST into GET | Browser page moves only |

## 9. Debugging and troubleshooting

**Browser fails, curl works.** Preflight or `Origin` not allowed. Fix allow-headers for `authorization` and `content-type`. Test OPTIONS.

**Lost update.** Two PUTs without `If-Match`. Require the validator and return `412`.

**Shared-computer back button shows an order.** Response was cacheable. Send `private, no-store`.

**401 loop.** Client never sends `Authorization` or `Cookie`, or `Path` does not match the route.

## 10. Interview preparation

**Beginner.** What is `WWW-Authenticate` for?  
**Model answer.** It is the `401` challenge that names acceptable auth schemes.  
**Incorrect.** "It sends the user's password."

**Intermediate.** Why is `no-cache` easy to misuse?  
**Model answer.** The name sounds like `no-store`, but RFC 9111 defines it as revalidate-before-reuse. Private data needs `no-store`.  
**Follow-up.** What is `304`? Validators match, so the body is omitted. It is not an error.

**Advanced.** Why is CORS not authentication?  
**Model answer.** Browsers use it to decide whether script may read a cross-origin response. Other HTTP clients ignore it. Object authorization still runs on every call.

**Scenario.** Missing tokens return `403`.  
**Model answer.** Clients will not start an authentication flow. Use `401` and `WWW-Authenticate`. Use `403` when identity is known and the action is forbidden.

## 11. Exercises and mastery assessment

1. Write headers for a conditional GET that returns `304`.
2. List session-cookie flags and one failure if each is missing.
3. Which status moves a POST endpoint permanently, and which status is unsafe for that job?
4. List the three steps of a CORS preflight.
5. Why does `If-Match` failure skip the write?

**Solutions.**

1. Request `If-None-Match: "rev-9"`. Response `304` with no body.
2. `HttpOnly` (script theft), `Secure` (cleartext theft), `SameSite` (cross-site send), tight `Path` (cookie on unrelated routes).
3. `308` preserves the method. `301` is the unsafe choice for a write.
4. Browser sends OPTIONS. Server returns allow-origin, methods, and headers. Browser sends the real request only if that passed.
5. The record changed after the client read it. Writing would drop the newer edit.

**Mastery checklist.**

- `401` plus challenge versus `403`.
- Cookie flags.
- `ETag`, `304`, `If-Match`.
- 307/308 versus 301/302.
- CORS is a browser policy.

**Revision summary.** Credentials are per request. Caches follow `Cache-Control` and validators. Redirect codes differ on whether the method survives. Preflight is an OPTIONS gate in the browser.

## Flashcards

- Q: What does `no-store` mean? | A: Do not store the response.
- Q: Which redirects preserve POST? | A: 307 and 308.
- Q: Who enforces CORS? | A: The browser.
