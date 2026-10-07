## Tests

```sh
python -m pip install -r requirements-test.txt
python -m pytest
```

These initial tests cover selected behavior with external services mocked. They do not establish full integration coverage.

Coverage: empty-contact behavior and per-contact message calls. All browser interactions are mocks; no WhatsApp messages are sent.
