from requests import get, post, delete

print(get('http://localhost:5000/api/person_base_info/1').json())

print(get('http://localhost:5000/api/person_pro_info/1').json())

print(get('http://localhost:5000/api/news/999').json())

print(get('http://localhost:5000/api/atribut_base_info/1').json())

print(get('http://localhost:5000/api/atribut_pro_info/1').json())

print(get('http://localhost:5000/api/atribut_pro_info/999').json())

print(post('http://localhost:5000/api/add_anecdot/слон на лоб').json())

# новости с id = 999 нет в базе