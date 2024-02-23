# FarmOn Coding Challenge

## Overview

Welcome to the FarmOn Coding Challenge! This challenge is designed to test your coding skills and your ability to apply them in the context of agriculture technology. FarmOn is focused on delivering farming insights, and this challenge reflects real-world scenarios you might encounter working with our technology and tech-stack.

## Challenge Description

### Objective
Develop an API endpoint that can integrate with FarmOn's system. This endpoint should return a single field for a given location with its carbon content and the carbon potential.

### Background
We would like to know how much carbon could be sequestrated on a field. You are given two datasets:
* Feld delinations for agricultural parcels in an area in the Netherlands. The dataset contains the following information:
  * Field ID
  * Field area
  * Field geometry
  * Crop type
* Soil organic carbon (SOC) measurements for the same area.

You can have a look at the data here: [01 - FarmOn Coding Challenge.ipynb](pipelines%2Fnotebooks%2F01%20-%20FarmOn%20Coding%20Challenge.ipynb)

### Challenge
1. Look at the data and come up with an idea on how to calculate the carbon potential for each field. The carbon potential is the difference between the current SOC and the SOC that could be stored in the soil.
3. Store the information in the MongoDB database using the [/parcels/add_parcels](http://localhost:8080/parcels/add_parcels) endpoint.
4. Implement an API endpoint [here](api/app/routers/parcels.py) that returns a single field for a given location with its carbon content and the carbon potential. Don't forget to write and run tests for the API endpoint.
5. Present the data through a simple UI. You can use any technology you like. The UI should be able to show the carbon content and the carbon potential for a given location. Integrate the UI into the current docker setup.


### Requirements

1. **API Integration**: Service the data through a RESTful API.
2. **Scalability and Efficiency**: Your code should be efficient and scalable to handle large datasets (every field in Europe, for example).
3. **Documentation**: Provide clear instructions on how to run your code and a brief explanation of your approach.
4. **Clarity and Readability**: Write clear, concise, and well-structured code.
5. **Testing**: It is not required to have 100% test coverage, but you should write tests for the API endpoint.

## Submission Guidelines

1. **Code Repository**: Submit your code in a Git repository (GitHub).
2. **Documentation**: Extend the README with:
   - Setup instructions
   - How to run the code
   - A brief explanation of your approach
   - A simple test case

## Evaluation Criteria

- **Code Quality**: Readability, structure, and adherence to standard practices.
- **Functionality**: Accuracy and efficiency of the module.
- **Innovation**: Creative solution and approache.
- **Scalability**: Ability to handle large datasets efficiently.

## Deadline

Submit your solution latest 5 working days after receiving the challenge.

## Questions

For any questions or clarifications, please contact [thimm@farmonapp.com](mailto:thimm@farmonapp.com).

Good luck, and we look forward to your innovative solutions!


## How to get started

1. Create a new branch
2. Run `docker compose --env-file .env.example up --build`
3. The API documentation is available on [http://localhost:8000/docs](http://localhost:8000/docs)
4. A jupyter lab instance is available on [http://localhost:8888](http://localhost:8888). Password is `farmon`


## Services
- **API**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Jupyter Lab**: [http://localhost:8888](http://localhost:8888)
- **MongoDB**: [http://localhost:27017](http://localhost:27017)
- **Mongo Express**: [http://localhost:8081](http://localhost:8081)

You can find the passwords in the [.env.example](.env.example) file.

## Tips
- Keep in mind that geo data has different types of projections. Make sure to use the right one for your calculations.
- When connecting to the API through jupyter lab, make sure to use the right URL. It should be `http://api:8080` instead of `http://localhost:8080`.