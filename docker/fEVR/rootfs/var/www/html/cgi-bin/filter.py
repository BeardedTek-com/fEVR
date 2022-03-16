#!/usr/bin/python

class eventFilter:
    def __init__(self,frigateURL,currentFilters):
        from logit import logit
        from os.path import basename
        self.script = basename(__file__)
        self.error = logit(debug=True)
        self.html = ""
        from frigateConfig import frigateConfig
        self.frigateConfig= frigateConfig(frigateURL)
        self.currentFilters = currentFilters
        self.filterOptions =    {   "count":  ["10","20","50","100"],
                                    "score":["60","70","80","90"],
                                    "time": ["1h","2h","6h","12h","1d","1w","1m"],
                                    "sort": ["newest first","oldest first"]
                                }
        self.filters = ""
        #self.filters = self.cameras + self.objects
        for filter in self.currentFilters:
            if filter == 'camera':
                output = self.Cameras()
            elif filter == 'type':
                output = self.Objects()
            elif filter == "sort":
                output = self.Sort()
            elif filter == "score":
                output = self.Score('score')
            else:
                output = self.Other(filter)
            self.filters += output

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
        SelectStub = "<select class='filterselect text-light-accent' name='camSelect' id='camSelect'>\n#CAMERAS#</select>\n"
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
        return SelectStub.replace('#CAMERAS#',Options)

    def Objects(self):
        SelectStub = "<select class='filterselect text-light-accent' name='objSelect' id='objSelect'>\n#OBJECTS#</select>\n"
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
        return SelectStub.replace('#OBJECTS#',Options)

    def Sort(self):
        SelectStub = "<select class='filterselect text-light-accent' name='objSelect' id='objSelect'>\n#SORTS#</select>\n"
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
        return SelectStub.replace('#SORTS#',Options)

    def Score(self,Filter):
        SelectStub = "<select class='filterselect text-light-accent' name='#TYPE#Select' id='#TYPE#Select'>\n#FILTERS#</select>\n"
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
        Options = Options.replace("#TYPE#",Filter)
        SelectStub = SelectStub.replace("#FILTERS#",Options)
        SelectStub = SelectStub.replace("#TYPE#",Filter)
        return SelectStub

    def Other(self,Filter):
        SelectStub = "<select class='filterselect text-light-accent' name='#TYPE#Select' id='#TYPE#Select'>\n#FILTERS#</select>\n"
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
        Options = Options.replace("#TYPE#",Filter)
        SelectStub = SelectStub.replace("#FILTERS",Options)
        SelectStub = SelectStub.replace("#TYPE#",Filter)
        return SelectStub

