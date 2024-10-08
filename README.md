# CheckMyReume
<h1>API's</h1>
<pre>
Regstration:
API: http://127.0.0.1:8000/register/ [POST,GET]
pass the data using form by using below keys
Data stores like this:
    {
        "name": "charan",
        "email": "22a51a42a0@adityatekkali.edu.in",
        "phone_number": "1234567891",
        "email_token": "3519614a-694d-4d24-b5d0-ff83d6ea4a81",
        "profile_image": "/media/profile/2_8SjRlRz.png"
    }
</pre>
<br>
<pre>
Login:
API: http://127.0.0.1:8000/login/ [POST]
Data should pass like this:
{
    "email":"22a51a42a0@adityatekkali.edu.in",
    "password":"12345"
}
</pre>
<br>
<pre>
Logout:
API: http://127.0.0.1:8000/logot/ [POST]
just sent a post request to this api 
</pre>
<br>
<pre>
Resume storage:
API: http://127.0.0.1:8000/resumestorage/ [POST,GET,DELETE]
pass only resume using form by using below keys
Data stores like this:
    {
        "id": 9,
        "resume": "/media/resume/AR20_DAA_Lab20CAL303_Manual_Final_1_T2wQjk8.pdf",
        "user": 7
    }
</pre>
<br>
<pre>
Resume Score storage:
API: http://127.0.0.1:8000/resumescorestorage/ [POST,GET,DELETE]
pass only resume using form by using below keys
Data stores like this:
    {
        "id": 9,
        "resume": "Resume score",
        "user": 7
    }
</pre>
