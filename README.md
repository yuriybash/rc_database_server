### Simple database server for RC

Running it locally (assuming your `python` is 2.7.x):

```
git clone git@github.com:yuriybash/rc_database_server.git
cd rc_database_server

# run the server
python main.py

curl http://localhost:4000/set?somekey=somevalue # OK
curl http://localhost:4000/get?key=somekey # somevalue
```


Running unit tests:
```
python setup.py test

running test
test_do_GET (tests.handlers.RequestHandlerTest) ... ok
...
test_store_multiple (tests.storage.InMemoryStorageTest) ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.007s

OK
```
