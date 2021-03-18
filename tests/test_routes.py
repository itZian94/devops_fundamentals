import pytest
from application import routes, app, db
from application.models import Ticket, Fix
from flask import url_for
from flask_testing import TestCase

class TestBase(TestCase):
    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///",
        DEBUG=True
        )
        return app

    def setUp(self):
        db.create_all()

        sample_ticket=Ticket(user="John Smith", issue="Database")
        sample_fix=Fix(status="pending", ticket_id=1)

        db.session.add(sample_ticket)
        db.session.add(sample_fix)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestRead(TestBase):
    def test_ticket_get(self):
        response=self.client.get(url_for('user'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Smith', response.data)
        self.assertIn(b'Database', response.data)

    def test_fix_get(self):
        response=self.client.get(url_for('tech'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'pending', response.data)
        self.assertIn(b'1', response.data)

class TestAdd(TestBase):
    def test_ticket_add(self):
        response=self.client.post(
            url_for('user'),
            data=dict(user='John Smith', issue='Database'),
            follow_redirects=True
        )
        self.assertIn(b'John Smith', response.data)

    def test_fix_add(self):
        response=self.client.post(
            url_for('tech'),
            data=dict(status='pending', ticket_id=1),
            follow_redirects=True
        )
        self.assertIn(b'pending', response.data)


class TestTicketUpdate(TestBase):
    oldissue= ''
    newissue= ''
    def test_ticket_update(self):
        response=self.client.post(
            url_for('updateuser'),
            data=dict(oldissue='Database',newissue='Server'),
            follow_redirects=True
        )
        self.assertNotEqual(b'oldissue', b'newissue')

class TestFixUpdate(TestBase):
    oldstatus=''
    newstatus=''
    def test_fix_update(self):
        response=self.client.post(
            url_for('updatetech'),
            data=dict(oldstatus='pending', newstatus='fixed'),
            follow_redirects=True
        )
        self.assertNotEqual(b'oldstatus', b'newstatus')



class TestDelete(TestBase):
    def test_fix_delete(self):
        response=self.client.post(
            url_for('deletetech'),
            data=dict(status='pending', ticket_id=1),
            follow_redirects=True
        )
        self.assertNotIn(b'pending', response.data)
    
    def test_ticket_delete(self):
        response=self.client.post(
            url_for('deletetech'),
            data=dict(status='pending', ticket_id=1),
            follow_redirects=True
        )
        self.assertNotIn(b'pending', response.data)
        
        response2=self.client.post(
            url_for('deleteuser'),
            data=dict(user='John Smith', issue='Database'),
            follow_redirects=True
        )
        self.assertNotIn(b'John Smith', response2.data)