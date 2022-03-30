curl -X POST -d '{"name":"Charmander"}' http://127.0.0.1:8000/pokemon/addpokemon/ -H 'Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ4NzU5MDkwLCJqdGkiOiJlYTBmOWE0ZjYyYzg0MmJiYTkwYzAwMDA4M2QzMTI5ZSIsInVzZXJfaWQiOjF9.tTMdjBtvr1IOWGaxKjDMcVtKSdjOqvLboB_jNSTD9d8' > apiresponse.html && open apiresponse.html

