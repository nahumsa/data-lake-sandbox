set_up:
	sudo mkdir minio
	sudo mkdir minio/data
	sudo chmod a+rwx /minio/data
run:
	docker-compose up -d
stop:
	docker-compose down
tear_down:
	sudo rm -r minio/