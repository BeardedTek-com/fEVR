#!/usr/bin/python

class eventFilter:
    def __init__(self,frigateURL,currentFilters,recordCount,selectors):
        from logit import logit
        from os.path import basename
        self.script = basename(__file__)
        self.error = logit(debug=True)
        self.html = ""
        self.recordCount = recordCount
        self.selectors = selectors
        from frigateConfig import frigateConfig
        self.frigateConfig= frigateConfig(frigateURL)
        self.currentFilters = currentFilters
        self.filterOptions =    {   "count":  ["10","20","50","100"],
                                    "score":["60","70","80","90"],
                                    "time": ["1h","2h","6h","12h","1d","1w","1m","1y"],
                                    "sort": ["CAMERA ASC","CAMERA DESC","OBJECT ASC","OBJECT DESC","SCORE ASC","SCORE DESC","TIME ASC","TIME DESC"]
                                }
        self.filters = ""
        #self.filters = self.cameras + self.objects

        # FIND OUT HOW MANY RECORDS WE'RE DEALING WITH...
        sql = f"""SELECT COUNT(*) from events"""
        wheres = {}
        for key in ['camera','type','score']:
            if self.currentFilters[key] != '':
                if key == 'score':
                    wheres[key] = f"""{key}>{self.currentFilters[key]}"""
                else:
                    wheres[key] = f"""{key}='{self.currentFilters[key]}'"""
                
        if self.currentFilters['time'] != '':
            value = self.currentFilters['time']
            from datetime import datetime, timedelta
            import time
            ctime = datetime.fromtimestamp(time.time())
            valueInt = int(value[:-1])
            if value[-1] == "d":
                ftime = ctime - timedelta(days=valueInt)
            elif value[-1] == "h":
                ftime = ctime - timedelta(hours=valueInt)
            elif value[-1] == "w":
                ftime = ctime - timedelta(weeks=valueInt)
            elif value[-1] == "y":
                valueInt = valueInt * 365
                ftime = ctime - timedelta(days=valueInt)
            if ftime != ctime:
                ftime = datetime.timestamp(ftime)
                self.error.execute(f"TIME: {key}>{ftime}",src=self.script)
                wheres['time'] = f""" time > {ftime}"""
        n = 0
        for key in wheres:
            if n != 0:
                prefix = " AND "
            else:
                prefix = " WHERE "
            sql+=f"""{prefix}{wheres[key]}"""
            n+=1
        sql+=""";"""
        from sqlite import sqlite
        fsqlite = sqlite()
        fsqlite.open()
        query = fsqlite.count(sql)
        self.error.execute(f"COUNT SQL: {sql}",src=self.script)
        self.error.execute(f"RESULTS : {query}",src=self.script)
        if str(query)[0:1] != "E":
            self.numRecords = int(query)
        else:
            self.numRecords = 0

        for filter in self.currentFilters:
            if filter == 'camera':
                output = self.Cameras()
            elif filter == 'type':
                output = self.Objects()
            elif filter == "sort":
                output = self.Sort()
            elif filter == "score":
                output = self.Score('score')
            elif filter == "page":
                output = ''
            else:
                output = self.Other(filter)
            self.filters += output

            self.pager = self.Pager()
    def setSelected(self,currentFilters,item,option):
        if str(currentFilters) != str(item):
            option = option.replace(" selected","")
            true = 0
        else:
            true = 1
        return {"value": option,"true": true}

    def remove_dup(self,a):
        i = 0
        while i < len(a):
            j = i + 1
            while j < len(a):
                if a[i] == a[j]:
                    del a[j]
                else:
                    j += 1
            i += 1

    def Cameras(self):
        SelectStub = "<span class='fieldSpan'><select onchange='filterEvents();' class='filterselect text-light-accent border-dark bg-dark-accent' name='camSelect' id='camSelect'>\n#CAMERAS#</select></span>\n"
        OptionStub = "\t<option value='#CAMERA#' selected>#CAMERA#</option>\n"
        Options = ""
        self.objects = []
        cameras = self.frigateConfig.cameras
        isthereone = 0
        for camera in cameras:
            # Loop through each camera in cameras and create a camOption
            camOption = OptionStub.replace('#CAMERA#',camera)
            selected = self.setSelected(self.currentFilters['camera'],camera,camOption)
            Options += selected['value']
            isthereone += selected['true']

            for object in cameras[camera]['objects']:
                self.objects.append(object)
            self.remove_dup(self.objects)
        if isthereone == 0:
            Options += OptionStub.replace('#CAMERA#','all cameras')
            Options = Options.replace("value='all cameras'", "value=''")
        else:
            Options += OptionStub.replace("'#CAMERA#' selected>#CAMERA#","''>all cameras")
        return SelectStub.replace('#CAMERAS#',Options)

    def Objects(self):
        SelectStub = "<span class='fieldSpan'><select onchange='filterEvents();' class='filterselect text-light-accent border-dark bg-dark-accent' name='objSelect' id='objSelect'>\n#OBJECTS#</select></span>\n"
        OptionStub = "\t<option value='#OBJECT#' selected>#OBJECT#</option>\n"
        Options = ""
        isthereone = 0
        for object in self.objects:
            objOption = OptionStub.replace('#OBJECT#',object)
            selected = self.setSelected(self.currentFilters['type'],object,objOption)
            Options += selected['value']
            isthereone += selected['true']
        if isthereone == 0:
            Options += OptionStub.replace('#OBJECT#','all objects')
            Options = Options.replace("value='all objects'", "value=''")
        else:
            Options += OptionStub.replace("'#OBJECT#' selected>#OBJECT#","''>all objects")

        return SelectStub.replace('#OBJECTS#',Options)

    def Sort(self):
        SelectStub = "<span class='fieldSpan'><select onchange='filterEvents();' class='filterselect text-light-accent border-dark bg-dark-accent' name='objSelect' id='objSelect'>\n#SORTS#</select></span>\n"
        OptionStub = "\t<option value='#SORT#' selected>#SORT#</option>\n"
        Options = ""
        isthereone = 0
        for object in self.objects:
            objOption = OptionStub.replace('#SORT#',object)
            selected = self.setSelected(self.currentFilters['type'],object,objOption)
            Options += selected['value']
            isthereone += selected['true']
        if isthereone == 0:
            Options = Options.replace("value='newest first'", "value='newest first' selected")
        else:
            Options += OptionStub.replace("'#SORTS#' selected>#SORTS#","''>sort by")
        return SelectStub.replace('#SORTS#',Options)

    def Score(self,Filter):
        SelectStub = "<span class='fieldSpan'><select onchange='filterEvents();' class='filterselect text-light-accent border-dark bg-dark-accent' name='#TYPE#Select' id='#TYPE#Select'>\n#FILTERS#</select></span>\n"
        OptionStub = "\t<option value='#FILTER#' selected>#FILTER#%</option>\n"
        Options = ""
        isthereone = 0
        Filter = Filter
        for filter in self.filterOptions[Filter]:
            Option = OptionStub.replace('#FILTER#',filter)
            selected = self.setSelected(self.currentFilters['score'],filter,Option)
            Options += selected['value']
            isthereone += selected['true']
        if isthereone == 0:
            Options += OptionStub.replace('#FILTER#','all #TYPE#s')
            Options = Options.replace("value='all #TYPE#s'", "value='0'")
            Options = Options.replace("selected>all #TYPE#s%","selected>all #TYPE#s")
        else:
            Options += OptionStub.replace("'#FILTER#' selected>#FILTER#","''>all #TYPE#s")
        Options = Options.replace("#TYPE#",Filter)
        SelectStub = SelectStub.replace("#FILTERS#",Options)
        SelectStub = SelectStub.replace("#TYPE#",Filter)
        return SelectStub

    def Other(self,Filter):
        if Filter == 'count':
            SelectStub = "<span class='fieldSpan'><select onchange='filterEvents();' class='filterselect text-light-accent border-dark bg-dark-accent' name='#TYPE#Select' id='#TYPE#Select'>\n#FILTERS#</select></span>\n"
            OptionStub = "\t<option value='#FILTER#' selected>#FILTER#/page</option>\n"
        else:
            SelectStub = "<span class='fieldSpan'><select onchange='filterEvents();' class='filterselect text-light-accent border-dark bg-dark-accent' name='#TYPE#Select' id='#TYPE#Select'>\n#FILTERS#</select></span>\n"
            OptionStub = "\t<option value='#FILTER#' selected>#FILTER#</option>\n"
        Options = ""
        isthereone = 0
        for filter in self.filterOptions[Filter]:
            Option = OptionStub.replace('#FILTER#',filter)
            selected = self.setSelected(self.currentFilters[Filter],filter,Option)
            Options += selected['value']
            isthereone += selected['true']
        if isthereone == 0:
            Options += OptionStub.replace('#FILTER#','all #TYPE#s')
            Options = Options.replace("value='all #TYPE#s'", "value=''")
        else:
            Options += OptionStub.replace("'#FILTER#' selected>#FILTER#","''>all #TYPE#s")
        Options = Options.replace("#TYPE#",Filter)
        SelectStub = SelectStub.replace("#FILTERS",Options)
        SelectStub = SelectStub.replace("#TYPE#",Filter)
        return SelectStub

    def Pager(self):
        if self.selectors['count'] == 'all':
            curPageOutput = f"<span class='pager'>1 of 1</span>"
            nextPageOutput = "<span class='pager disabled'>next</span>"
            prevPageOutput = "<span class='pager disabled'>prev</span>"
        else:
            curPage = int(self.selectors['page'])
            self.page = curPage
            self.countPerPage = int(self.selectors['count'])
            from math import ceil
            pageCount = ceil(int(self.numRecords)/self.countPerPage)
            curPageOutput = f"<span class='pager'>{curPage} of {pageCount}</span>"
            nextPageOutput = "<span class='pager disabled'>next</span>"
            prevPageOutput = "<span class='pager disabled'>prev</span>"
            if self.recordCount > int(self.currentFilters['page']):
                pageCounter = pageCount
                baseURL = "?"
                for selector in self.selectors:
                    if selector != 'page':
                        baseURL += f"{selector}={self.selectors[selector]}&"
                self.pager = []
                self.pager.append('PAD ZERO')
                pageNum = 0
                
                while pageCounter > 0:
                    pageNum += 1
                    self.pager.append(f"<span class='pager'><a href='{baseURL}page={pageNum}'>#PAGE#</a>")
                    pageCounter -= 1
                if curPage > 1:
                    prevPage = curPage - 1
                    prevPageOutput = self.pager[prevPage].replace('#PAGE#','prev')
                nextPage = curPage + 1
                if nextPage <= pageCount:
                    nextPageOutput = self.pager[nextPage].replace('#PAGE#','next')
        return f"{prevPageOutput} {curPageOutput} {nextPageOutput}"
