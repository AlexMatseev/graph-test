# Application for working with graphs

## The graph contains 2 types of nodes. 1 type - vector. That is, a sequence of numbers should be set in these nodes. 2 node type - operation (addition,multiplication, etc.)

## Recalculation of values is provided due to changes in the parent node (vector or operator)

### Install

* Clone a repository 
```git clone ```
* If the Pipenv library is not installed, install it with the command:
<br /> MacOs:  ```brew install pipenv```
<br /> Ubuntu:
```
$ sudo apt install software-properties-common python-software-properties
$ sudo add-apt-repository ppa:pypa/ppa
$ sudo apt update
$ sudo apt install pipenv
```
<br />Windows and others:  ```pip install pipenv```

* Install all dependencies ```pipenv sync```
* Creating migrations ```python manage.py makemigrations```
* Application of migrations ```python manage.py migrate```
* Launching the application ```python manage.py runserver```

<br /> The list of all nodes is located at /api/
<br />  The documentation is located at /redoc/ or /swagger/
### Example  of creating a graph

* Move to url ```api/create/vector```
* Create fist vector: In the input form, specify the value of the vector in comma-separated digits (for example, 1,1,1)
*  Create second vecor: In the input form, specify the value of the vector in comma-separated digits (for example, 1,1,1)
* Move to url ```api/create/operator```
* Select the operator value from the list
* Viewing the graph structure is implemented by the url ```/api/```
* To update the vector value, go to the url ```update/vector/<int:pk>/``` where pk is the id of the vector
*To update the operator value, go to the url ```update/operator/<int:pk>/``` where pk is the operator id
* Deleting specific vectors and operators is carried out by the corresponding urls: ```delete/vector/<int:pk>/``` and ```delete/operator/<int:pk>/```, where pk is the id of the graph element
