# First dropdown:
# How many: [“column”]
# Have : {“ column”}
# “Greater than/less than” {“value from column”}
# “Equal t
# o”AND/OR (repeat)
# "Get everything from": ["{column}"],
# "What is": ["the sum", "the max", "the min", "the average"]}
# “The sum” : “of {column}”


# “The max”: “of {column}”
# “The min”: “of {column}”
# “The average”: “of {column}”
# “Get the” [“{column}"]
# ‘That have:  {“ column”}
# “Greater than/less than” {“value from column”}
# “Equal t
# o”AND/OR (repeat)

# Dropdown workflow:
# [“Get the”, “How many”, “What is”, “Get everything from”]
from makedb import query_db
from SqlBuilder import SqlBuilder

class StructuredNLP():
    # on page load, return phraseTree["origin"]
    phraseTree = {"origin": ["Get the", "How many", "What is", "Get everything from"],
                  "Get the": "columns",
                  "How many": "columns",
                  "Get everything from": "columns",
                  "What is": ["the sum", "the max", "the min", "the average"]}

    def __init__(self, tableName, colLabels):
        self.isPastWhere = False
        self.tableName = tableName

        self.returnedColumn = False # last set of options user saw was list of
        self.prevColumn = '' # if self.returnedColumn, what that column value was

        self.firstColumn = True
        self.allColumns = colLabels

        self.sqlBuilder = SqlBuilder(tableName)


    def updatePossibleSelections(self, choice):
        if choice == "where":
            self.isPastWhere = True

        if self.isPastWhere:  # filtering out (THE LOOP)
            if self.firstColumn:
                self.firstColumn = False
                self.returnedColumn = True
                self.sqlBuilder.hitWhere()
                return self.appendWithIs(self.getAllColumns())

            if not self.returnedColumn:
                self.returnedColumn = True
                self.sqlBuilder.addColumnValue(choice)
                return self.appendWithIs(self.prependWithAnd(self.getAllColumns()))
            else:  # we are filling in WHERE self.currentColumns [is/isgreater than????]
                self.returnedColumn = False
                self.sqlBuilder.addColumn(choice)
                return self.getColumnValues(choice)
        else:  # in initial projection/question selection
            if self.returnedColumn:
                # return [AND + columns..., WHERE]
                self.sqlBuilder.addColumn(choice)
                return ["where"] + self.prependWithAnd(self.getAllColumns())
                # output.append("where")
                # return output
            else:
                phraseTreeValue = self.phraseTree[choice]
                if phraseTreeValue == "columns":
                    self.sqlBuilder.baseSQLQuery(choice)
                    self.returnedColumn = True
                    return self.getAllColumns()
                else:
                    return self.phraseTree[choice] # very first step only


    def getAllColumns(self):
        return self.allColumns

    def getColumnValues(self, columnString):
        column = columnString.split(" ")[-2]
        query = "SELECT " + column + " FROM " + self.tableName + ";"
        queryResult = query_db(query)
        return list(set([str(item).lstrip().strip() for sublist in queryResult for item in sublist]))

    def prependWithAnd(self, allColumns):
        return ['and {0}'.format(i) for i in allColumns]

    def appendWithIs(self, allColumns):
        return ['{0} is'.format(i) for i in allColumns]

    def runQuery(self):
        print(query_db(self.sqlBuilder.getQuery()))
        return query_db(self.sqlBuilder.getQuery())
