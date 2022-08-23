# ToDo Rest API #

According requirements, here is my submission for the REST API to do app!

# Stack #
Made using Chalice for serverless/lambda/API gateway and DynamoDB for data storage.

# To run locally #
Please create a PY3.9 env and install all dependencies on requirements.txt 
```bash
pip install -r requirements.txt
```

To run it locally issue on the terminal: 

```bash
chalice local
```

To run tests:
```bash
pytest -vv
```

To access the API via swagger:

Just control+c control+v the ```task_02.yml``` file into [SWAGGER_EDITOR](https://editor.swagger.io/) and you
should be good to go (PS: that's why the flag cors=True on the app views.)
