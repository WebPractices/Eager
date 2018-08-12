from pymongo import MongoClient


class MongodbClient(object):

    def __init__(self, table, host, port):
        self.table = table
        self.client = MongoClient(host, port)
        self.db = self.client.eager

    def change_table(self, table):
        self.table = table

    def get(self, num):
        data = self.db[self.table].find_one({'num': num})
        return data if data != None else None

    def put(self, data):
        if self.exists(data):
            return None
        count = self.get_nums
        data['num'] = count + 1
        self.db[self.table].insert_one(data)

    def delete(self, num):
        self.db[self.table].remove({'num': num})

    def get_batch(self, start, end):
        """
        batch get data by a interval
        :param start: start num
        :param end: end num
        """
        if not isinstance(start, int) and isinstance(end, int):
            return None
        return [data for data in self.db[self.table].find().limit(start).skip(end)]

    def clean(self, db):
        self.client.drop_database(db)

    def delete_all(self):
        self.db[self.table].remove()

    def update(self, num, data):
        self.db[self.table].update({'num': num}, {'$set': data})

    def exists(self, data):
        if self.table == 'novel':
            if self.db[self.table].find_one(
                    {'name': data['name'], 'author': data['author']}):
                return True
        else:
            if self.db[self.table].find_one(
                    {'novel': data['novel'], 'title': data['title']}):
                return True
        return False

    @property
    def get_nums(self):
        return self.db[self.table].count()


if __name__ == "__main__":
    db = MongodbClient('first', 'localhost', 27017)
    # db.put('127.0.0.1:1')
    # db2 = MongodbClient('second', 'localhost', 27017)
    # db2.put('127.0.0.1:2')

