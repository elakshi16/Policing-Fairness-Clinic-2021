# Policing-Fairness-Clinic-2021

Docker environment for running policing-fairness clinic models.

**Steps to run:**

1. in terminal run `docker-compose build`
    
2. `docker-compose up`
    
3. Follow URL provided in terminal. password: `policing`

**Steps to end session**
1. `Ctrl+C` to close docker container

**To edit**

Add python packages to requirements.txt

Any new `*.py` files should be importable modules

For running tests:
1. Create test-specific notebook (either your name, or run name)
2. Import required modules
3. Execute tests & make use of notebook's documentation features