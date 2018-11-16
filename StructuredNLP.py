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
                  "How many": "columns",
                  "Get everything from": "columns",
                  "what is": ["the sum", "the max", "the min", "the average"]}

    def __init__(self):
        self.projectColumns = []
        self.isPastWhere = False

    def addProjectionColumn(self, projCol):
        self.projectColumns.append(projCol)

    def updatePossibleSelections(self, choice, column=False):
        if choice == "where":
            self.isPastWhere = True
            return self.getAllColumns()

        if self.isPastWhere:  # filtering out (THE LOOP)
            if not column:
                return self.getAllColumns()
            else:  # we are filling in WHERE self.currentColumns [is/isgreater than????]
                return self.getColumnValues(choice)
        else:  # in initial projection/question selection
            if column:

                self.projectColumns.append(choice)
                return self.getAllColumns()

            else:
                return self.phraseTree[choice]

        nextOptions = self.phraseTree[choice]

        return formatOptions(nextOptions)


    def getAllColumns(self):
        pass

        # TODO

    def getColumnValues(self, column):
        pass

        # TODO


    def formatOptions(self, opts):
        if "columns" == opts:
            # get columns
            return self.getAllColumns()
        elif "columnValues" == opts:
            pass
            # return self.getColumnValues(currentColumns)
        else:
            return opts



