producer-java:
	cd java-producer &&	gradle run

connect-postgres:
	docker exec -it postgres psql -U postgres -h localhost -d app_db