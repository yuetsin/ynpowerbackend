clear classes
obj = py.importlib.import_module('interface');
py.importlib.reload(obj);
result = py.interface.getData("yunnan_year_电力电量类", "consumption", "2008", "2016")