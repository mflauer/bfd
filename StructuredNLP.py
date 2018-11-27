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


class structuredNLP():
    # on page load, return phraseTree["origin"]
    phraseTree = {"origin": ["Get the", "How many", "What is", "Get everything from"],
                  "Get the": "columns",
                  "How many": "columns",
                  "Get everything from": "columns",
                  "What is": ["the sum", "the max", "the min", "the average"]}

    def __init__(self):
        self.isPastWhere = False
        self.tableName = ''
        self.returnedColumn = False # last set of options user saw was list of columns
        self.firstColumn = True

    def setTableName(self, tableName):
        self.tableName = tableName

    def updatePossibleSelections(self, choice):
        if choice == "where":
            self.isPastWhere = True

        if self.isPastWhere:  # filtering out (THE LOOP)
            if self.firstColumn:
                self.firstColumn = False

                self.returnedColumn = True
                return self.appendWithIs(self.getAllColumns())

            if not self.returnedColumn:
                self.returnedColumn = True
                return self.appendWithIs(self.prependWithAnd(self.getAllColumns()))
            else:  # we are filling in WHERE self.currentColumns [is/isgreater than????]
                self.returnedColumn = False
                return self.getColumnValues(choice)
        else:  # in initial projection/question selection
            if self.returnedColumn:
                # return [AND + columns..., WHERE]
                return self.prependWithAnd(self.getAllColumns()) + ["where"]
                # output.append("where")
                # return output
            else:
                phraseTreeValue = self.phraseTree[choice]
                if phraseTreeValue == "columns":
                    self.returnedColumn = True
                    return self.getAllColumns()
                else:
                    return self.phraseTree[choice]


    def getAllColumns(self):
        return ['col1', 'col2', 'col3']

    def getColumnValues(self, column):
        return ['val1', 'val2', 'val3']

    def prependWithAnd(self, allColumns):
        return ['and {0}'.format(i) for i in allColumns]

    def appendWithIs(self, allColumns):
        return ['{0} is'.format(i) for i in allColumns]