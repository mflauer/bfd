
class SqlBuilder():

    def __init__(self, tableName):
        self.query = ""
        self.tableName = tableName
        self.didHitWhere = False

        self.baseTree = {"Get the": "SELECT ",
                    "How many " + tableName + " entries are there where": "SELECT COUNT(*)"}

    def baseSQLQuery(self, choice):
        self.query += self.baseTree[choice]

    def addAggregate(self, aggType, column):
        aggSQL = aggType
        if aggType == "average":
            aggSQL = "avg"

        print(aggType)
        print(column)
        self.query = "SELECT " + aggSQL + "(" + column + ")"

    def hitWhere(self):
        self.didHitWhere = True
        self.query += " FROM " + self.tableName + " WHERE "

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


    def addColumnValue(self, val):
        self.query += " = '" + val + "' "

    def getQuery(self):
        return self.query + ";"

