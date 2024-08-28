# aham_fund_mgt
Backend Developer Practical: A simple Fund Management System written with Flask


How to start?
```python
# Build images
docker-compose build

# Migrate tables
docker-compose run web pipenv run flask db upgrade

# Start
docker-compose up
```

# Funds APIs
### You may test these APIs by importing this [postman_link](https://api.postman.com/collections/9329394-484881ce-4fc9-4128-90e4-7da02cb819b5?access_key=PMAT-01J6AG3KSMBMZZ6JCFY4PSTMCF) to your collection

| Resource            | API                                |
| :----------------   | :----------------------------------|
| Fetch funds         | GET localhost:5001/funds           |
| Fetch single fund   | GET localhost:5001/funds/:uuid     |
| Create fund         | POST localhost:5001/funds          |
| Update fund         | PUT localhost:5001/funds/:uuid     |
| Delete fund         | DELETE localhost:5001/funds/:uuid  |

# Data migration to MySQL
```
# Execute migration program
docker-compose run web pipenv run python migrate_funds.py

# Verify in DB
docker-compose exec db mysql -u user -p -e "USE fund_mgt_development; SELECT * FROM funds;"
password: password
```

# Specs
```
pipenv run pytest
```

# References to each tasks
### Task 1
- [models/fund.py](https://github.com/mirulzuan/aham_fund_mgt/blob/main/app/models/fund.py)
### Task 2
- [routs/fund_route.py](https://github.com/mirulzuan/aham_fund_mgt/blob/main/app/routes/fund_route.py)
### Task 3
- [config.py](https://github.com/mirulzuan/aham_fund_mgt/blob/main/config.py#L7)
### Task 4
- [schemas/fund_schema.py](https://github.com/mirulzuan/aham_fund_mgt/blob/main/app/schemas/fund_schema.py)
### Task 5
- [migrate_funds.py](https://github.com/mirulzuan/aham_fund_mgt/blob/main/migrate_funds.py)
### Task 6
- [routs/fund_route.py](https://github.com/mirulzuan/aham_fund_mgt/blob/main/app/routes/fund_route.py)
- [migrate_funds.py](https://github.com/mirulzuan/aham_fund_mgt/blob/main/migrate_funds.py)
### Task 7
- [tests/routes/fund_route_test.py](https://github.com/mirulzuan/aham_fund_mgt/blob/main/app/tests/routes/fund_route_test.py)
### Task 8
- Code comments
- This Readme section
