# z-test

#### Run locally
```
docker-compose up
docker compose exec web python manage.py migrate 
```
After that project is available at http://0.0.0.0:8000/v1/api/

### Work flow
 - For adding new site for image scrapping go to http://0.0.0.0:8000/v1/api/url/ ;  example POST data format `{"url": "https://commons.wikimedia.org/wiki/File:JPEG_example_flower.jpg"}`
 - For viewing all scrapped data go to http://0.0.0.0:8000/v1/api/image/.
 - Quering image:
    - GET http://0.0.0.0:8000/v1/api/image/{image_id} for viewing individual image data.
    - GET http://0.0.0.0:8000/v1/api/image/?size={small/mediam/large}  for viewing data based on image size. 
    - GET http://0.0.0.0:8000/v1/api/image/?url=https://commons.wikimedia.org/wiki/File:JPEG_example_flower.jpg  for viewing data based on scrapped site
 
### Known limitations
 - The current implementation doesn't support sites that use client side rendering.
 - For simplicity, this implementation is only parsing jpg files.  
