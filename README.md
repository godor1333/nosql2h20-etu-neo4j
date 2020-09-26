# nosql2h20-etu-neo4j
### Development
1. ```git clone https://github.com/moevm/nosql2h20-etu-neo4j```
1. ```cd nosql2h20-etu-neo4j```
1. ```docker-compose up```
1. ```docker ps```
1. Find ID of the container with the web application.
1. Apply constraints or indexes by ```docker exec -it 9ed93c3e921a neomodel_install_labels uemployees/db.py --db bolt://neo4j:@neo4j:7687```
1. Now service is available at **127.0.0.1:8000**