


class SqlBuilder():

    baseTree = {"Get the": "SELECT ", }
                  # "How many": "columns",
                  # "Get everything from": "columns",
                  # "What is": ["the sum", "the max", "the min", "the average"]}

    def __init__(self, tableName):
        self.query = ""
        self.tableName = tableName
        self.didHitWhere = False

    def baseSQLQuery(self, choice):
        self.query += self.baseTree[choice]
        print(self.query)

    def hitWhere(self):
        self.didHitWhere = True
        self.query += " FROM " + self.tableName + " WHERE "
        print(self.query)

    def addColumn(self, col):
        if self.didHitWhere:
            col = " ".join(col.split(" ")[:-1])
            self.query += col
        else:
            if len(col.split(" ")) == 2:
                col = col.split(" ")[-1]
                self.query += ", " + col
            else:
                self.query += col
        print(self.query)


    def addColumnValue(self, val):
        self.query += " = '" + val + "' "
        print(self.query)

    def getQuery(self):
        print(self.query)
        return self.query

