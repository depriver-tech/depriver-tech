from common import lesson as L
BOOK=dict(slug='python-backend',title='Python for Backend',subtitle='Flask, FastAPI and dependable service design.',color='#4E4C85',
 intro='Build JSON services with Flask and FastAPI, then learn the engineering decisions around them: validation, storage, access control, transactions, retries, testing and deployment. Small examples keep the concepts visible. The final task-service project connects the pieces without pretending that a classroom demo is a production platform.',
 prerequisite='Know Python functions, dictionaries and exceptions. Basic HTTP knowledge helps; the first lessons explain the service contract. The Python for Web book covers HTML websites, while this book focuses on machine-readable interfaces and backend behaviour.',
 setup='Create a virtual environment using python -m venv .venv. Activate it with source .venv/bin/activate on macOS/Linux or .venv\\Scripts\\activate.bat in Windows Command Prompt. Install the packages below. Run each file independently; framework examples include in-process requests. Never deploy hardcoded demonstration credentials.',
 install='python -m pip install Flask "fastapi[standard]" httpx\npython lesson_01_example.py\npython lesson_01_solution.py',
 refs=[('Flask API','https://flask.palletsprojects.com/en/stable/api/'),('FastAPI tutorial','https://fastapi.tiangolo.com/tutorial/'),('FastAPI security','https://fastapi.tiangolo.com/tutorial/security/'),('FastAPI deployment','https://fastapi.tiangolo.com/deployment/'),('SQLite transactions','https://docs.python.org/3/library/sqlite3.html'),('HTTP semantics','https://www.rfc-editor.org/rfc/rfc9110.html')],lessons=[])
A=BOOK['lessons']
A.append(L('Design an API contract','State what a client sends and what it receives.',
'An API contract describes paths, methods, input shapes, responses and failures. Start with the user task before choosing framework syntax. GET reads; POST commonly creates or triggers work; PUT replaces a representation; PATCH changes selected fields; DELETE removes a resource. Exact semantics must be documented and tested.',
'''contract = {
    "GET /tasks": {"status": 200, "body": {"items": []}},
    "POST /tasks": {"status": 201, "required": ["title"]},
    "GET /tasks/unknown": {"status": 404},
}
assert contract["POST /tasks"]["status"] == 201
assert "title" in contract["POST /tasks"]["required"]''',
'This executable dictionary is a design note, not a running server. It forces you to choose response behaviour before implementation details obscure it.',
'Define response envelopes for a successful item and a missing item. Keep the public error message separate from internal debugging information.',
['Success contains id and title','Missing item has a stable error code','No traceback or credential in the error'],
'Use a small error object whose keys remain consistent across routes.',
'''def success(ident, title):
    return {"item": {"id": ident, "title": title}}
def missing():
    return {"error": {"code": "not_found",
                      "message": "Task not found"}}
assert success(1, "Learn")["item"]["id"] == 1
assert missing()["error"]["code"] == "not_found"
assert "traceback" not in str(missing()).lower()''',
'A stable shape makes client code simpler. The HTTP status is still needed; an error envelope returned with 200 can mislead clients and monitoring.',
'Changing field names without coordinating clients is an API change even when the server still runs.',
'Write three request-and-response examples for a future task API, including one validation failure.'))
A.append(L('Flask JSON endpoints','Return structured data with explicit status codes.',
'Flask can serialise dictionaries as JSON. Keep route functions small: read input, call domain logic and build a response. A JSON API does not need HTML templates. The response content type matters because clients need to know how to parse the body.',
'''from flask import Flask
app = Flask(__name__)
@app.get("/health")
def health():
    return {"status": "ok"}
c = app.test_client()
r = c.get("/health")
assert r.status_code == 200
assert r.is_json
assert r.json == {"status": "ok"}''',
'The test checks status, format and payload. A route returning the string representation of a dictionary would not be equivalent JSON.',
'Add a read-only item endpoint with a 404 response for an unknown ID. Keep error bodies JSON too.',
['Known ID -> 200 JSON','Missing ID -> 404 JSON','No HTML error page for this handled failure'],
'Return a tuple containing the response dictionary and status.',
'''from flask import Flask
app = Flask(__name__)
@app.get("/items/<int:ident>")
def item(ident):
    if ident != 1:
        return {"error": "not_found"}, 404
    return {"id": 1, "title": "Notebook"}
c = app.test_client()
assert c.get("/items/1").json["title"] == "Notebook"
r = c.get("/items/99")
assert r.status_code == 404 and r.is_json''',
'This route handles its own missing-record case. A complete API also needs a consistent policy for routing failures and unexpected errors.',
'Flask returning JSON does not automatically validate every incoming payload.',
'Add a list endpoint and test that its empty state is an empty array inside a stable envelope.'))
A.append(L('FastAPI and typed paths','Use declared types to validate request structure.',
'FastAPI reads type annotations and declarations to validate inputs and generate an OpenAPI description. A type declaration communicates a contract, but domain rules still need explicit checks. Path parsing errors and missing database records are different failures.',
'''from fastapi import FastAPI
from fastapi.testclient import TestClient
app = FastAPI()
@app.get("/double/{value}")
def double(value: int):
    return {"result": value * 2}
c = TestClient(app)
assert c.get("/double/3").json() == {"result": 6}
assert c.get("/double/abc").status_code == 422''',
'The framework rejects a value that cannot be parsed as an integer before the handler runs. Test the behaviour that your clients will see rather than assuming all bad inputs become 400.',
'Create an endpoint that squares a non-negative path value. Return 400 for a negative integer and allow zero.',
['/square/4 -> 16','/square/0 -> 0','/square/-1 -> 400','/square/text -> 422'],
'Raise HTTPException for the domain rule after successful type parsing.',
'''from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
app = FastAPI()
@app.get("/square/{value}")
def square(value: int):
    if value < 0:
        raise HTTPException(400, "Use a non-negative value")
    return {"result": value * value}
c = TestClient(app)
assert c.get("/square/4").json()["result"] == 16
assert c.get("/square/0").json()["result"] == 0
assert c.get("/square/-1").status_code == 400
assert c.get("/square/text").status_code == 422''',
'Framework validation checks representation; your function checks meaning. Keep those responsibilities clear when documenting errors.',
'Type hints on an ordinary Python function do not validate its arguments by themselves.',
'Inspect /openapi.json and identify the declared path parameter and response operations.'))
A.append(L('Request models','Validate a document before modifying state.',
'Pydantic models describe structured request bodies. Declare bounds and field types close to the API boundary. Validation should happen before database writes or external calls. Decide whether unknown fields are accepted or rejected so clients do not silently send misspelled properties.',
'''from pydantic import BaseModel, Field, ConfigDict
class TaskInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=2, max_length=80)
    priority: int = Field(ge=1, le=5)

task = TaskInput(title="Learn", priority=2)
assert task.priority == 2
assert task.model_dump()["title"] == "Learn"''',
'The model constrains length and numeric range. A whitespace-only title can still pass a length test, so normalisation and domain validation remain important.',
'Create a model that strips whitespace and rejects a blank title. Add tests for a valid title, blank input and an unknown field.',
['"  Learn  " -> "Learn"','Spaces only -> validation error','Extra field -> validation error'],
'Use str_strip_whitespace in model configuration plus min_length.',
'''from pydantic import BaseModel, Field, ConfigDict, ValidationError
class TaskInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    title: str = Field(min_length=1, max_length=80)
assert TaskInput(title="  Learn  ").title == "Learn"
for data in [{"title": "   "}, {"title": "A", "unknown": 1}]:
    try:
        TaskInput(**data)
    except ValidationError:
        pass
    else:
        raise AssertionError("Invalid payload accepted")''',
'The boundary converts accepted input into a predictable model. Tests demonstrate both normalisation and rejection, which are different promises.',
'Coercion may accept values you expected to reject. Use strict types when that matches the contract and test examples explicitly.',
'Add an optional due date and reject dates that violate a clearly stated business rule.'))
A.append(L('Response models','Control which fields cross the service boundary.',
'Internal records may contain private fields or implementation details. A response model defines the public view and reduces accidental exposure. Do not return an entire user or database object merely because serialisation is convenient. Add fields deliberately and document their meaning.',
'''from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
class PublicUser(BaseModel):
    id: int
    name: str
app = FastAPI()
@app.get("/me", response_model=PublicUser)
def me():
    return {"id": 1, "name": "Asha", "secret": "internal"}
r = TestClient(app).get("/me")
assert r.json() == {"id": 1, "name": "Asha"}''',
'The response model excludes the secret field from this response. Authorisation still decides whether the caller should see even the public fields.',
'Define a public task response that exposes id, title and done, while excluding owner_token from an internal record.',
['Public fields are present','owner_token is absent','JSON done is a boolean'],
'Use a separate model instead of reusing a database model with every column.',
'''from pydantic import BaseModel
class PublicTask(BaseModel):
    id: int
    title: str
    done: bool
internal = {"id": 1, "title": "Read", "done": False,
            "owner_token": "private"}
public = PublicTask(**internal).model_dump()
assert public == {"id": 1, "title": "Read", "done": False}
assert "owner_token" not in public''',
'Separate input, internal and output shapes as the application grows. A field allowed in a response is not necessarily editable by the caller.',
'Redacting only in the UI is too late: the network response has already exposed the data.',
'Write a regression test that fails if a new internal credential field appears in API output.'))
A.append(L('Separate service logic','Keep business rules testable without HTTP.',
'A route should translate transport details, while a service function enforces domain rules. This keeps validation consistent across HTTP, command-line tools and background jobs. Avoid hiding every decision inside decorators or database queries.',
'''def create_task(title, priority):
    title = title.strip()
    if not title:
        raise ValueError("Title required")
    if priority not in range(1, 6):
        raise ValueError("Priority must be 1-5")
    return {"title": title, "priority": priority, "done": False}
assert create_task("  Learn  ", 2)["title"] == "Learn"''',
'The function knows nothing about Flask or FastAPI. A route can convert ValueError into the agreed HTTP error without duplicating the underlying rule.',
'Implement a transition that completes a task and rejects an attempt to complete it twice. Return a new record instead of changing the original.',
['Incomplete -> completed copy','Original remains incomplete','Already completed -> ValueError'],
'Check the rule first, then copy with a dictionary expansion.',
'''def complete(task):
    if task["done"]:
        raise ValueError("Already completed")
    return {**task, "done": True}
original = {"id": 1, "done": False}
updated = complete(original)
assert updated["done"] and not original["done"]
try:
    complete(updated)
except ValueError:
    pass
else:
    raise AssertionError("Repeated transition accepted")''',
'This is one chosen domain policy. Another API might deliberately make completing an already-complete task idempotent; choose and document it.',
'Framework-neutral code can still have hidden dependencies if it reads globals or environment variables internally.',
'Pass a clock function into a service that records completion time so tests can use a fixed timestamp.'))
A.append(L('Persistence and SQL','Use database constraints to support application rules.',
'A database stores durable state and can enforce uniqueness and required values. Application checks improve messages, while database constraints protect integrity under concurrency. Parameterised SQL handles values safely. Keep connection lifetime and transaction boundaries explicit.',
'''import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, "
            "title TEXT NOT NULL UNIQUE)")
con.execute("INSERT INTO tasks(title) VALUES (?)", ("Read",))
con.commit()
assert con.execute("SELECT title FROM tasks").fetchone() == ("Read",)
con.close()''',
'The primary key identifies rows and the uniqueness constraint rejects duplicate titles in this specific design. Real task systems may allow repeated titles and use a different uniqueness rule.',
'Insert a duplicate title, catch the integrity error and confirm that there is still only one stored row.',
['First insert succeeds','Duplicate insert raises IntegrityError','Count remains one'],
'Catch sqlite3.IntegrityError and roll back the failed transaction.',
'''import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE tasks(title TEXT UNIQUE)")
con.execute("INSERT INTO tasks VALUES (?)", ("Read",))
con.commit()
try:
    con.execute("INSERT INTO tasks VALUES (?)", ("Read",))
    con.commit()
except sqlite3.IntegrityError:
    con.rollback()
assert con.execute("SELECT COUNT(*) FROM tasks").fetchone()[0] == 1
con.close()''',
'Integrity rules belong in storage as well as application code because two requests can pass an existence check at the same time.',
'An in-memory database is a teaching fixture, not durable storage across process restarts.',
'Move this example to a temporary file and reopen the connection to prove committed data persists.'))
A.append(L('Transactions and rollback','Keep related writes all-or-nothing.',
'A transaction groups changes that must succeed together. If one step fails, rollback prevents a partially updated state. Keep transactions short and avoid waiting for external services while holding locks. A remote API call and a database transaction do not automatically form one atomic operation.',
'''import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE stock(id INTEGER PRIMARY KEY, qty INTEGER)")
con.execute("INSERT INTO stock VALUES (1, 5)")
con.commit()
try:
    with con:
        con.execute("UPDATE stock SET qty = qty - 1 WHERE id = 1")
        raise RuntimeError("Simulated failure")
except RuntimeError:
    pass
assert con.execute("SELECT qty FROM stock").fetchone()[0] == 5
con.close()''',
'The connection context rolls back when the exception escapes the block. Closing the connection is still a separate responsibility.',
'Use a conditional update to reserve one unit only when stock is positive. Verify the second reservation fails when only one unit existed.',
['Initial stock 1 -> first reservation succeeds','Second reservation -> no row changed','Final stock is 0, never negative'],
'Put qty > 0 in the UPDATE condition and inspect rowcount.',
'''import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE stock(id INTEGER PRIMARY KEY, qty INTEGER)")
con.execute("INSERT INTO stock VALUES (1, 1)")
con.commit()
def reserve():
    with con:
        result = con.execute("UPDATE stock SET qty=qty-1 "
                             "WHERE id=1 AND qty>0")
        return result.rowcount == 1
assert reserve()
assert not reserve()
assert con.execute("SELECT qty FROM stock").fetchone()[0] == 0
con.close()''',
'The condition and update happen in one SQL statement, avoiding a separate read-then-write gap. Wider workflows may need stronger isolation or locking policies.',
'Catching an exception inside the transaction and suppressing it can accidentally allow a commit unless you roll back deliberately.',
'Add a reservation record in the same transaction and prove that failure of either write restores the previous state.'))
A.append(L('Authentication boundaries','Verify who is calling before doing protected work.',
'Authentication establishes a caller identity. A simple service-to-service API key is different from a complete user login system. Store real secrets outside source code, compare carefully, rotate them and require HTTPS. User passwords should use a maintained password-hashing implementation rather than a home-made hash.',
'''from hmac import compare_digest

def authenticated(expected, supplied):
    return bool(expected and supplied) and compare_digest(
        expected, supplied)
assert authenticated("local-demo-key", "local-demo-key")
assert not authenticated("local-demo-key", "wrong")
assert not authenticated("", "")''',
'This helper demonstrates a credential comparison, not a full authentication platform. It has no rate limiting, expiry, audit trail or user account recovery.',
'Create a FastAPI dependency that rejects a missing or incorrect X-API-Key. Use a fixed key only inside this isolated test.',
['Missing key -> 401','Wrong key -> 401','Correct demonstration key -> 200'],
'Use Header and Depends so protected endpoints share the check.',
'''from fastapi import FastAPI, Header, Depends, HTTPException
from fastapi.testclient import TestClient
from hmac import compare_digest
app = FastAPI()
def owner(x_api_key: str = Header(default="")):
    if not compare_digest(x_api_key, "local-demo-key"):
        raise HTTPException(401, "Authentication required")
@app.get("/private", dependencies=[Depends(owner)])
def private():
    return {"ok": True}
c = TestClient(app)
assert c.get("/private").status_code == 401
assert c.get("/private", headers={"X-API-Key": "wrong"}).status_code == 401
assert c.get("/private", headers={
    "X-API-Key": "local-demo-key"}).status_code == 200''',
'In deployment, read the expected key from a secret store and fail closed if it is missing. The demo constant is intentionally not a real credential.',
'Putting an API key into browser JavaScript makes it available to every visitor; it cannot protect a private owner API.',
'Add credential rotation and tests proving both the missing-secret and wrong-secret paths deny access.'))
A.append(L('Authorisation and ownership','Check what an authenticated caller may do.',
'Authorisation is separate from authentication. A valid user must not gain access to another user\'s record just by guessing its ID. Check ownership or permissions at the service boundary on every protected operation. Hiding a button in the UI is not an access-control check.',
'''def can_read(user_id, task):
    return task["owner_id"] == user_id

task = {"id": 9, "owner_id": 2, "title": "Private"}
assert can_read(2, task)
assert not can_read(3, task)''',
'The user identifier must come from trusted authentication, not a body field supplied by the caller.',
'Return a task only when its owner matches the authenticated user. Use the same not-found response for absent and inaccessible records in this exercise.',
['Owner gets the task','Other user receives None','Missing ID receives None'],
'Look up the record, then compare ownership before returning it.',
'''def find_owned(tasks, ident, user_id):
    task = tasks.get(ident)
    if task is None or task["owner_id"] != user_id:
        return None
    return task

tasks = {1: {"id": 1, "owner_id": 7, "title": "Read"}}
assert find_owned(tasks, 1, 7)["title"] == "Read"
assert find_owned(tasks, 1, 8) is None
assert find_owned(tasks, 99, 7) is None''',
'Returning the same public result for absence and denied ownership can reduce information leakage. Internal logs can still record the actual reason without revealing private data to the caller.',
'A request body containing owner_id is not proof of ownership. Derive it from the authenticated principal.',
'Add a shared-read permission and test that it does not accidentally grant write access.'))
A.append(L('Pagination and filters','Bound work per request and return stable results.',
'An API that returns every record can become slow or exhaust memory. Validate limits, establish stable ordering and document pagination. Offset pagination is simple; cursor pagination can use a unique increasing key to continue from the last returned record.',
'''def after_id(rows, cursor=0, limit=2):
    if not 1 <= limit <= 100:
        raise ValueError("Limit must be 1-100")
    ordered = sorted(rows, key=lambda row: row["id"])
    return [row for row in ordered if row["id"] > cursor][:limit]
rows = [{"id": 3}, {"id": 1}, {"id": 2}]
assert after_id(rows, 1) == [{"id": 2}, {"id": 3}]''',
'This list-based example teaches cursor meaning. A database implementation should push filtering, ordering and limit into SQL rather than loading the full table.',
'Return an items envelope and next_cursor only when more rows remain. Read one extra matching row to decide whether there is another page.',
['Three rows, limit 2 -> cursor 2','Last page -> cursor None','Empty input -> empty items and None'],
'Slice limit + 1 rows, return only limit, and use the last returned ID when an extra row exists.',
'''def page(rows, cursor=0, limit=2):
    if not 1 <= limit <= 100:
        raise ValueError("Invalid limit")
    found = [r for r in sorted(rows, key=lambda r: r["id"])
             if r["id"] > cursor][:limit+1]
    items = found[:limit]
    nxt = items[-1]["id"] if len(found) > limit else None
    return {"items": items, "next_cursor": nxt}
rows = [{"id": 1}, {"id": 2}, {"id": 3}]
assert page(rows)["next_cursor"] == 2
assert page(rows, 2)["next_cursor"] is None
assert page([])["items"] == []''',
'A unique key makes the continuation unambiguous. If ordering uses a non-unique timestamp, include an ID tie-breaker in the cursor.',
'A cursor should represent the chosen ordering, not an unrelated count or page label.',
'Add a filter and explain whether changing it invalidates an existing cursor.'))
A.append(L('Idempotency and retries','Make repeated requests safe when a response is lost.',
'A client may retry because it never received the response, even though the server completed the action. Idempotency keys let the server recognise a repeated logical request. Store the key, request identity and result atomically in durable storage. A simple in-memory example only demonstrates the idea.',
'''results = {}
def create_once(key, title):
    if key in results:
        old_title, result = results[key]
        if old_title != title:
            raise ValueError("Key reused with different input")
        return result
    result = {"id": len(results) + 1, "title": title}
    results[key] = (title, result)
    return result
assert create_once("abc", "Read") == create_once("abc", "Read")
assert len(results) == 1''',
'The same key and input reuse the result; the same key with different input is rejected. A real implementation must also handle two requests arriving at once.',
'Write a retry wrapper that retries only a declared transient exception and gives up after a fixed attempt count. Do not sleep in this test.',
['Immediate success -> one call','Two transient failures -> third call succeeds','Permanent exception -> no retry'],
'Catch only the transient exception and re-raise on the last attempt.',
'''def retry(operation, attempts=3):
    if attempts < 1:
        raise ValueError("At least one attempt")
    for attempt in range(attempts):
        try:
            return operation()
        except TimeoutError:
            if attempt == attempts - 1:
                raise
calls = []
def flaky():
    calls.append(1)
    if len(calls) < 3:
        raise TimeoutError()
    return "ok"
assert retry(flaky) == "ok"
assert len(calls) == 3''',
'Production retries also need backoff, jitter and a total deadline. Retrying a non-idempotent action without a server-side policy can duplicate work.',
'Do not retry every exception: invalid input will not improve after waiting.',
'Test a failing operation that always times out and confirm exactly the configured number of attempts.'))
A.append(L('Dependencies and test doubles','Replace external dependencies without rewriting handlers.',
'Dependency injection supplies a collaborator instead of creating it deep inside a function. It makes behaviour easier to test with a fixed clock, fake repository or controlled HTTP client. FastAPI offers dependency overrides; ordinary Python functions can simply accept arguments.',
'''def report(clock):
    return {"generated_at": clock(), "status": "ok"}
assert report(lambda: "2026-10-19T00:00:00Z") == {
    "generated_at": "2026-10-19T00:00:00Z", "status": "ok"}''',
'The test is deterministic because time is an input. Hidden reads of the current time would make exact output harder to reproduce.',
'Create a FastAPI route with an injected repository function, then override it in a test to return a controlled record.',
['Override returns the test record','Route uses the dependency rather than a global lookup','Override can be cleared after the test'],
'Assign the replacement callable to app.dependency_overrides.',
'''from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
app = FastAPI()
def repository():
    return {"title": "Default"}
@app.get("/task")
def task(record=Depends(repository)):
    return record
app.dependency_overrides[repository] = lambda: {"title": "Test"}
assert TestClient(app).get("/task").json() == {"title": "Test"}
app.dependency_overrides.clear()''',
'The route is tested against a controlled dependency. Separate integration tests are still needed for the real database or external service.',
'A test double that always returns ideal data can hide errors in the real integration contract.',
'Add tests where the repository reports not-found and where it raises an expected availability error.'))
A.append(L('Async without confusion','Distinguish waiting from CPU-heavy computation.',
'Async code lets one task yield while waiting for another operation. It does not make expensive Python calculations automatically faster. Use await with non-blocking clients; calling blocking code inside an async handler can block the event loop. Synchronous handlers may be the clearer choice for synchronous libraries.',
'''import asyncio
async def fetch_label(label):
    await asyncio.sleep(0)
    return label.upper()
async def main():
    return await asyncio.gather(fetch_label("a"), fetch_label("b"))
assert asyncio.run(main()) == ["A", "B"]''',
'The zero-duration sleep yields control without introducing a real delay. gather collects results in input order, not completion order.',
'Limit concurrent operations to two using a semaphore. Track active operations and assert that the limit is never exceeded.',
['Every job returns a result','Maximum active operations <= 2','No operation remains active after completion'],
'Use async with semaphore and decrement the active counter in finally.',
'''import asyncio
async def main():
    limit = asyncio.Semaphore(2)
    active = peak = 0
    async def work(value):
        nonlocal active, peak
        async with limit:
            active += 1
            peak = max(peak, active)
            try:
                await asyncio.sleep(0)
                return value * 2
            finally:
                active -= 1
    result = await asyncio.gather(*(work(i) for i in range(5)))
    assert peak <= 2 and active == 0
    return result
assert asyncio.run(main()) == [0, 2, 4, 6, 8]''',
'A concurrency limit protects a downstream system and your own resources. It is different from a requests-per-second rate limit.',
'Creating thousands of unbounded tasks can overload a service even if every call is non-blocking.',
'Add cancellation handling and a total timeout, then verify cleanup still runs.'))
A.append(L('Background jobs','Separate a quick acknowledgement from durable work.',
'Long-running work should often be queued rather than keeping an HTTP request open. A background task in the same process can disappear if that process stops. Durable queues need job IDs, states, retries and idempotent processing. A 202 response means accepted, not completed.',
'''jobs = {}
def submit(ident):
    jobs.setdefault(ident, {"state": "queued", "attempts": 0})
    return {"job_id": ident, "state": jobs[ident]["state"]}
assert submit("report-1")["state"] == "queued"
assert submit("report-1")["job_id"] == "report-1"
assert len(jobs) == 1''',
'The dictionary models states only. It is not durable and does not coordinate multiple workers. The same job ID does not create a second job in this simplified example.',
'Implement legal transitions queued -> running -> succeeded or failed. Reject a second start after completion.',
['Queued can start','Running can succeed or fail','Succeeded cannot return to running'],
'Use a transition map and validate before assignment.',
'''ALLOWED = {"queued": {"running"},
           "running": {"succeeded", "failed"},
           "succeeded": set(), "failed": set()}
def transition(job, state):
    if state not in ALLOWED[job["state"]]:
        raise ValueError("Invalid transition")
    return {**job, "state": state}
job = transition({"state": "queued"}, "running")
job = transition(job, "succeeded")
assert job["state"] == "succeeded"
try:
    transition(job, "running")
except ValueError:
    pass
else:
    raise AssertionError("Transition accepted")''',
'A state machine makes retry and recovery decisions visible. A failed job may be retried through a separate explicitly defined transition or a new attempt record.',
'An HTTP success code for job submission must not be displayed as proof that the report or email already completed.',
'Design a status endpoint and define how a worker recovers a job abandoned in running state.'))
A.append(L('Caching and invalidation','Reuse results without confusing old data with current truth.',
'A cache stores a result for reuse. It needs a key, expiry policy and invalidation strategy. Cached public data can improve performance, while a wrong key can expose another user\'s information. Keep authoritative state in durable storage; cache entries should be disposable.',
'''def cache_key(user_id, filters):
    return user_id, tuple(sorted(filters.items()))
assert cache_key(1, {"done": False}) != cache_key(2, {"done": False})
assert cache_key(1, {"a": 1, "b": 2}) == cache_key(1, {"b": 2, "a": 1})''',
'The key includes the user scope and canonicalised filters. This example assumes all values are hashable and the chosen filters fully describe the response.',
'Create a small time-to-live cache with an injected clock value. Expired entries should behave as misses.',
['Before expiry -> cached value','At expiry -> miss','Unknown key -> miss'],
'Store value and expires_at together and compare now < expires_at.',
'''class Cache:
    def __init__(self):
        self.data = {}
    def put(self, key, value, now, ttl):
        self.data[key] = (value, now + ttl)
    def get(self, key, now):
        value, expiry = self.data.get(key, (None, 0))
        return value if now < expiry else None
c = Cache()
c.put("public", "report", now=10, ttl=5)
assert c.get("public", 14) == "report"
assert c.get("public", 15) is None
assert c.get("missing", 14) is None''',
'The test avoids real sleeping by supplying time. A production cache also needs eviction, concurrency handling and a decision about whether None can be a stored value.',
'Caching an authorisation decision for too long can preserve access after permissions change.',
'Add explicit invalidation after a successful task update and test that stale data is no longer returned.'))
A.append(L('Logs and error handling','Record enough context to investigate without exposing secrets.',
'Logs should connect events to a request or job and distinguish expected failures from bugs. Use structured fields where possible. Avoid recording passwords, tokens or full private payloads. Return a safe public message while retaining appropriate internal diagnostics.',
'''import json
record = {"event": "task_created", "request_id": "req-1",
          "task_id": 7, "status": 201}
line = json.dumps(record, sort_keys=True)
assert json.loads(line)["request_id"] == "req-1"
assert "password" not in line''',
'The record describes the operation without storing the submitted body. A request identifier lets several log entries be connected.',
'Redact known sensitive top-level fields before serialising a diagnostic record. Do not mutate the original dictionary.',
['token and password values become [redacted]','Other fields remain','Original values are unchanged'],
'Build a new dictionary with a small explicit sensitive-key set.',
'''def redact(record):
    sensitive = {"token", "password", "authorization"}
    return {key: "[redacted]" if key.casefold() in sensitive else value
            for key, value in record.items()}
source = {"token": "secret", "event": "login"}
clean = redact(source)
assert clean == {"token": "[redacted]", "event": "login"}
assert source["token"] == "secret"''',
'This exercise handles only top-level known fields. Real logging policies should avoid collecting secrets in the first place and account for nested data and free text.',
'A redaction helper is not a guarantee that every possible secret has been removed.',
'Add a request ID middleware and confirm that responses and logs share the same generated identifier.'))
A.append(L('Configuration and releases','Separate code from deployment-specific values.',
'Configuration includes database locations, allowed origins and secrets. Read required values at startup and fail clearly if they are missing. A release needs repeatable dependencies, migrations, health checks and a rollback plan. Backups are only useful when restoration has been tested.',
'''def settings(env):
    database = env.get("DATABASE_URL")
    if not database:
        raise ValueError("DATABASE_URL is required")
    return {"database_url": database,
            "debug": env.get("DEBUG", "false").lower() == "true"}
assert settings({"DATABASE_URL": "sqlite:///local.db"})["debug"] is False''',
'Passing a mapping into the settings function makes startup rules testable without changing the real environment.',
'Validate a comma-separated allowed-origin configuration. Reject wildcard origins for this credentialed application policy.',
['Two origins -> two trimmed values','Wildcard -> ValueError','Empty configuration -> ValueError'],
'Parse, trim, then validate; do not silently substitute a permissive default.',
'''def allowed_origins(raw):
    origins = [part.strip() for part in raw.split(",") if part.strip()]
    if not origins or "*" in origins:
        raise ValueError("Explicit origins required")
    return origins
assert allowed_origins("https://a.test, https://b.test") == [
    "https://a.test", "https://b.test"]
for raw in ["", "*"]:
    try:
        allowed_origins(raw)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid origin policy")''',
'CORS controls which browser origins can read a response; it is not authentication and does not stop direct non-browser requests.',
'Deploying with DEBUG=true can expose internals even when the application otherwise works.',
'Write a release runbook with migration, smoke test, rollback and backup-restoration steps.'))
A.append(L('Tests at different boundaries','Match each test to a specific risk.',
'Unit tests check domain rules. Integration tests check databases and framework wiring. End-to-end tests check a real user or client journey. Use temporary data and isolated application instances. A test suite is useful when failures tell you which promise broke.',
'''def total(amounts):
    if any(value < 0 for value in amounts):
        raise ValueError("Negative amount")
    return sum(amounts)
assert total([]) == 0
assert total([2, 3]) == 5
try:
    total([-1])
except ValueError:
    pass
else:
    raise AssertionError("Negative amount accepted")''',
'These checks use known expected results. A test that computes the expected value with the exact same implementation can repeat the same mistake.',
'Write a FastAPI integration test for valid, invalid and missing input on a simple calculation endpoint.',
['Valid input -> expected result','Wrong type -> 422','Missing parameter -> 422'],
'TestClient lets you make requests without a live server.',
'''from fastapi import FastAPI
from fastapi.testclient import TestClient
app = FastAPI()
@app.get("/total")
def total(a: int, b: int):
    return {"total": a + b}
c = TestClient(app)
assert c.get("/total?a=2&b=3").json() == {"total": 5}
assert c.get("/total?a=x&b=3").status_code == 422
assert c.get("/total?a=2").status_code == 422''',
'The framework boundary is now tested as a client sees it. Add a real-server smoke test during deployment to catch routing, proxy or configuration problems.',
'Passing in-process tests does not prove that the public hostname, TLS or cloud database is configured correctly.',
'Create an acceptance matrix for the task API: anonymous, owner, other user, invalid payload and missing record.'))
A.append(L('Project: a task API','Build a small service and state its limits honestly.',
'The project creates tasks and retrieves them by ID. This local version uses an in-memory store so you can focus on validation and responses. It is not durable, authenticated or safe for multi-process deployment. The extension path replaces storage and adds ownership checks before public release.',
'''from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field, ConfigDict
class TaskInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str = Field(min_length=1, max_length=80)
app = FastAPI()
tasks = {}
@app.post("/tasks", status_code=201)
def create(body: TaskInput):
    ident = len(tasks) + 1
    tasks[ident] = {"id": ident, "title": body.title}
    return tasks[ident]
c = TestClient(app)
assert c.post("/tasks", json={"title": " Read "}).json() == {
    "id": 1, "title": "Read"}
assert c.post("/tasks", json={"title": " "}).status_code == 422''',
'The example handles creation only. The lab adds retrieval and checks the full create-then-read path in a standalone application.',
'Build creation and retrieval together. Verify a missing task gives 404, valid creation gives 201 and a read returns the created title.',
['POST valid title -> 201','GET returned ID -> same title','GET unknown ID -> 404','Blank title -> 422'],
'Use HTTPException for missing records and a Pydantic request model for validation.',
'''from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field, ConfigDict
class TaskInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str = Field(min_length=1, max_length=80)
app, tasks = FastAPI(), {}
@app.post("/tasks", status_code=201)
def create(body: TaskInput):
    ident = len(tasks) + 1
    tasks[ident] = {"id": ident, "title": body.title}
    return tasks[ident]
@app.get("/tasks/{ident}")
def read(ident: int):
    if ident not in tasks:
        raise HTTPException(404, "Task not found")
    return tasks[ident]
c = TestClient(app)
r = c.post("/tasks", json={"title": "Learn"})
assert r.status_code == 201
assert c.get("/tasks/1").json()["title"] == "Learn"
assert c.get("/tasks/99").status_code == 404
assert c.post("/tasks", json={"title": " "}).status_code == 422''',
'The create/read contract is verified. len(tasks)+1 works only for this no-delete, single-process demonstration. Use database-generated identifiers in a persistent service.',
'Do not call a demo production-ready merely because its happy path works. Authentication, ownership, persistence and operational checks remain separate deliverables.',
'Finish a persistent version with SQLite, owner checks, pagination, response models and integration tests. Write down every remaining limitation in its README.'))
assert len(A)==20
