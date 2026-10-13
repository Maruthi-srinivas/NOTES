# Flashcards

Extracted from chapters that define a Flashcards section, plus the protocol set below.

## Auth Headers, Cookies, Caching, Redirects, and CORS

- Q: What does `no-store` mean? | A: Do not store the response.
- Q: Which redirects preserve POST? | A: 307 and 308.
- Q: Who enforces CORS? | A: The browser.

## Index Design, Pagination Cost, and Query Security

- Q: Why cap `limit`? | A: One request must not be able to scan and serialize the whole table.
- Q: What is wrong with `LIKE '%x'`? | A: A btree index on the column cannot serve a leading wildcard.

## Negative, Boundary, Load, Compatibility, and Regression Tests

- Q: What does a boundary test hit? | A: The documented minimum and maximum, and one step past them.
- Q: What makes a load number believable? | A: The scenario, data size, concurrency, environment, and percentile.

## Roles, Scopes, Ownership, Tenancy, Cookies, and OIDC

- Q: What does a scope check prove? | A: The token was granted that scope. Not that this row belongs to the caller.
- Q: Who verifies an OIDC ID token? | A: Your server, against the issuer's keys, audience, and expiry.

## OpenAPI Security, Auth Tests, and Failure Handling

- Q: What does a security requirement in OpenAPI mean? | A: Callers must satisfy that scheme for this operation.
- Q: Why test with two users? | A: To prove object authorization, not only that a token parses.

