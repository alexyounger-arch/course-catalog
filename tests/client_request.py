
class ClientRequest:
    """Class to simplify the request"""

    @classmethod
    def add_course(cls, client, course, start_date, end_date, num_of_lecture):
        data = {'course': course, 'start_date': start_date, 'end_date': end_date, 'num_of_lecture': num_of_lecture}
        return client.post('/add-course', json=data)

    @classmethod
    def get_course(cls, client, id_):
        return client.get('/get-course', json={'id': id_})

    @classmethod
    def get_courses(cls, client):
        return client.get('/get-courses')

    @classmethod
    def get_filtered_courses(cls, client, course, start_date, end_date):
        data = {'course': course, 'start_date': start_date, 'end_date': end_date}
        return client.get('/get-filtered-courses', json=data)

    @classmethod
    def set_attribute(cls, client, id_, attribute, value):
        data = {'attribute': attribute, 'value': value, 'id': id_}
        return client.put('/set-attribute', json=data)

    @classmethod
    def delete_course(cls, client, id_):
        return client.delete('/delete-course', json={'id': id_})
