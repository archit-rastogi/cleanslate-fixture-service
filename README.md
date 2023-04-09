# cleanslate-fixture-service
Service to host cleanslate fixture apis


* strategical
  1. Build e2e soft testing platform


* sub-problems
  1. Share and consume fixtures - manually or via tests
  2. Share and consume mocks of their service

* Requirements
1. A fixture is identified by a unique id.
2. A running fixture is identified by unique_id and session_id.
3. A fixture has associated scope and cardinality.
   - scope: env_id
   - cardinalty: number of allowed running instances at any time
4. Fixture has a runtime state -> requested, queued, assigned, running, fulfilled, failed, aborted, completed
5. Fixture has properties.
   1. status: stable, unstable, deprecated, deleted
   2. tags
   3. owner, signed, etc.
   4. capacity
6. Fixture apis
   1. get
   2. details
   3. request
   4. status
   5. yield
7. Fixture impl defines below interfaces:
   1. setup and teardown
   2. monitoring
      1. health
      2. users
      3. status
