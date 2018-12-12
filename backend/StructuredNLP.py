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

    def __init__(self, tableName, colLabels, isColNumeric):
        self.isPastWhere = False
        self.tableName = tableName
        self.prevAgg = False

        self.returnedColumn = False # last set of options user saw was list of
        self.prevColumn = '' # if self.returnedColumn, what that column value was

        self.firstColumn = True
        self.allColumns = colLabels
        self.isColNumeric = isColNumeric
        self.returned_digit = False
        self.order_by = False

        self.sqlBuilder = SqlBuilder(tableName)
        # on page load, return phraseTree["origin"]
        self.phraseTree = {"origin": ["Get the", "How many " + tableName + " entries are there where",
                                      "What is", "What are the top", "What are the bottom"],
                        "Get the": "columns",
                        "How many " + tableName + " entries are there where":  "where",
                        "What is": ["the sum of", "the max of", "the min of", "the average of"],
                        "What are the top": "integer",
                        "What are the bottom": "integer",
                        "the sum of": "agg",
                        "the max of": "agg",
                        "the min of": "agg",
                        "the average of": "agg", }


    def updatePossibleSelections(self, choice):
        if choice == "where":
            self.isPastWhere = True

        if self.returned_digit:
            self.sqlBuilder.setLimit(choice.split(" ")[0])
            self.returned_digit = False
            self.order_by = True
            return self.getNumericColumns()

        if self.order_by:
            self.order_by = False
            self.sqlBuilder.insertColumn(choice)
            return []

        if self.prevAgg:
            self.sqlBuilder.addAggregate(self.prevAgg, choice.split(" ")[0])
            self.prevAgg = False
            return self.updatePossibleSelections("where")

        if self.isPastWhere:  # filtering out (THE LOOP)
            if self.firstColumn:
                self.firstColumn = False
                self.returnedColumn = True
                self.sqlBuilder.hitWhere()
                return self.appendWith(self.getAllColumns(), "is")

            if not self.returnedColumn:
                self.returnedColumn = True
                self.sqlBuilder.addColumnValue(choice)
                return self.appendWith(self.prependWith(self.getAllColumns(), "and"), "is")
            else:  # we are filling in WHERE self.currentColumns [is/isgreater than????]
                self.returnedColumn = False
                self.sqlBuilder.addColumn(choice)
                return self.getColumnValues(choice)
        else:  # in initial projection/question selection
            if self.returnedColumn:
                # return [AND + columns..., WHERE]
                self.sqlBuilder.addColumn(choice)
                return ["where"] + self.prependWith(self.getAllColumns(), "and")

            else:
                phraseTreeValue = self.phraseTree[choice]

                if phraseTreeValue == "integer":
                    self.sqlBuilder.baseSQLQuery(choice)
                    integers = ["3", "5", "10", "50", "100"]
                    self.returned_digit = True
                    return self.appendWith(integers, self.tableName + " entries by")

                elif phraseTreeValue == "agg":
                    self.prevAgg = choice.split(" ")[1]
                    return self.appendWith(self.getNumericColumns(), "where")

                elif phraseTreeValue == "where":
                    self.sqlBuilder.baseSQLQuery(choice)
                    return self.updatePossibleSelections(phraseTreeValue)

                elif phraseTreeValue == "columns":
                    self.sqlBuilder.baseSQLQuery(choice)
                    self.returnedColumn = True
                    return self.getAllColumns()

                else:
                    return self.phraseTree[choice]


    def getAllColumns(self):
        return self.allColumns

    def getNumericColumns(self):
        numericCols = []
        for i in range(len(self.allColumns)):
            if self.isColNumeric[i]:
                numericCols.append(self.allColumns[i])
        return numericCols

    def getColumnValues(self, columnString):
        column = columnString.split(" ")[-2]
        query = "SELECT " + column + " FROM " + self.tableName + ";"
        queryResult = query_db(query, self.tableName, False)
        return list(set([str(item) for sublist in queryResult for item in sublist]))

    def prependWith(self, allColumns, prependage):
        return ['{} {}'.format(prependage, i) for i in allColumns]

    def appendWith(self, allColumns, appendage):
        return ['{} {}'.format(i, appendage) for i in allColumns]

    def runQuery(self):
        return query_db(self.sqlBuilder.getQuery(), self.tableName, True)

    def resetQuery(self):
        self.isPastWhere = False

        self.returnedColumn = False  # last set of options user saw was list of
        self.prevColumn = ''  # if self.returnedColumn, what that column value was

        self.firstColumn = True

        self.sqlBuilder = SqlBuilder(self.tableName)
        return


