from ast import IsNot
from fileinput import filename
import os
from shutil import SpecialFileError
from sys import prefix
from tkinter import N
from xml.etree import ElementTree as ET
from numpy import empty, full
import pandas as pd


def getFullClassPath(unit):
    return unit.get('filename')

def totalClass(units):
    return len(units)

def isPublicMethod():
    return True

        


def extractMethods(units, ns):

    fullclasspath = []
    className = []
    isInnerClass = []
    methodName = []
    isPublicMethod = []
    isPrivateMethod = []
    isProtectedMethod = []
    isStaticMethod = []
    isAbstractMethod = []
    returnType = []
    numParameters = []
    numIntParams = []
    numStringParams = []
    numBooleanParams = []
    numByteParams = []
    numShortParams = []
    numLongParams = []
    numCharParams = []
    numDoubleParams = []
    numFloatParams = []
    numObjectParams = []
    isOverrideMethod = []
    #methodLOC = []

    exprelist = [
        'srcml:class/srcml:block/srcml:function',
        'srcml:interface/srcml:block/srcml:function',
        'srcml:enum/srcml:block/srcml:function'
    ]

    for unit in units:
        print("processing....")

        # ------- get class name ------
        _isInnerClass = False
        token = unit.get('filename').split('.') 
        if len(token) > 2:
            # inner class detected, set to true
            _isInnerClass = True
             # get the class name by removing .java
            _className = token[-2]
        else:
            # split the token and get the last element
            _className = token[0].split('\\')[-1]

        
        # -------- extends ------
        # class extended by current class instance
        
    

        # ------ method expression ---------
        for expression in exprelist:
            for methods in unit.findall(expression , ns):

                # full class path
                _fullclasspath = getFullClassPath(unit)

                # get class name



                # get method name 
                _methodName = methods.find('srcml:name', ns).text

                # method publicity 
                expr = methods.findall("srcml:specifier", ns)
                _isPublicMethod = False
                _isPrivateMethod = False
                _isProtectedMethod = False
                _isStaticMethod = False
                _isAbstractMethod = False

                for value in expr:
                    
                    if value is not None:
                        specifier = value.text

                        if specifier == "public": _isPublicMethod  = True
                        if specifier == "private": _isPrivateMethod  = True
                        if specifier == "protected": _isProtectedMethod  = True
                        if specifier == "static": _isStaticMethod  = True
                        if specifier == "abstract": _isAbstractMethod  = True
                
                # get method return type
                _returnType = methods.find('srcml:type/srcml:name', ns).text 
                if _returnType is None: 
                    _returnType = "None"
                

                # count the number of parameters in a method
                params = methods.findall('srcml:parameter_list/srcml:parameter', ns)
                params_name = methods.findall('srcml:parameter_list/srcml:parameter/srcml:decl/srcml:type/srcml:name', ns)
                _numParameters = len(params)

                 # ----------- split types of parameters ---------------
                _numIntParams = 0
                _numStringParams = 0
                _numBooleanParams = 0
                _numByteParams = 0
                _numShortParams = 0
                _numLongParams = 0
                _numCharParams = 0
                _numDoubleParams = 0
                _numFloatParams = 0
                _numObjectParams = 0
                # -------------------------------------------------

                for item in params_name:
                    try:
                        if item is not None:
                            # type_of_param = item.find('srcml:decl/srcml:type/srcml:name', ns).text
                            type_of_param = item.text
                            if type_of_param == "int":
                                _numIntParams += 1
                            if type_of_param == "String":
                                _numStringParams += 1
                            if type_of_param == "boolean":
                                _numBooleanParams += 1
                            if type_of_param == "byte":
                                _numByteParams += 1
                            if type_of_param == "short":
                                _numShortParams += 1
                            if type_of_param == "long":
                                _numLongParams += 1
                            if type_of_param == "char":
                                _numCharParams += 1
                            if type_of_param == "double":
                                _numDoubleParams += 1
                            if type_of_param == "float":
                                _numFloatParams += 1
                            if type_of_param not in ['int', 'String', 'boolean', 'byte', 'short', 'long', 'char', 'double', 'float', 'None']:
                                _numObjectParams += 1
                    except:
                        print("error")

                # determine if the method is overriden
                _isOverrideMethod = False
                check_override = methods.find('srcml:annotation/srcml:name', ns)
                
                if check_override is not None and check_override.text == "Override":
                    _isOverrideMethod = True     
                

                # calculate the loc within a method
                # NOT YET COMPLETED
                # method_block = methods.find('srcml:block', ns)
                # if method_block is not None:
                #     _methodLOC = len(method_block)

                
                # output in csv


                # outPutBuilder(
                #     fullclasspath = fullclasspath,
                #     methodName = methodName,
                #     isPublicMethod = isPublicMethod,
                #     isPrivateMethod = isPrivateMethod,
                #     isProtectedMethod = isProtectedMethod,
                #     isStaticMethod = isStaticMethod,
                #     isAbstractMethod = isAbstractMethod,
                #     returnType = returnType,
                #     numParameters = numParameters
                # )

                fullclasspath.append(_fullclasspath)
                className.append(_className)
                isInnerClass.append(_isInnerClass)
                methodName.append(_methodName)
                isPublicMethod.append(_isPublicMethod)
                isPrivateMethod.append(_isPrivateMethod)
                isProtectedMethod.append(_isProtectedMethod)
                isStaticMethod.append(_isStaticMethod)
                isAbstractMethod.append(_isAbstractMethod)
                returnType.append(_returnType)
                numParameters.append(_numParameters)
                numIntParams.append(_numIntParams)
                numStringParams.append(_numStringParams)
                numBooleanParams.append(_numBooleanParams)
                numByteParams.append(_numByteParams)
                numShortParams.append(_numShortParams)
                numLongParams.append(_numLongParams)
                numCharParams.append(_numCharParams)
                numDoubleParams.append(_numDoubleParams)
                numFloatParams.append(_numFloatParams)
                numObjectParams.append(_numObjectParams)
                isOverrideMethod.append(_isOverrideMethod)
                # methodLOC.append(_methodLOC)

    data = {
            'fullclasspath': fullclasspath,
            'className': className,
            'isInnerClass': isInnerClass,
            'methodName': methodName,
            'isPublicMethod': isPublicMethod,
            'isPrivateMethod': isPrivateMethod,
            'isProtected': isProtectedMethod, 
            'isStatic': isStaticMethod, 
            'isAbstractMethod': isAbstractMethod,
            'returnType': returnType,
            'numParameters': numParameters,
            'numIntParams': numIntParams,
            'numStringParams': numStringParams,
            'numBooleanParams': numBooleanParams,
            'numByteParams': numByteParams,
            'numShortParams': numShortParams,
            'numLongParams': numLongParams,
            'numCharParams': numCharParams,
            'numDoubleParams': numDoubleParams,
            'numFloatParams': numFloatParams,
            'numObjectParams': numObjectParams,
            'isOverrideMethod': isOverrideMethod,
            # 'methodLOC': methodLOC
    }

    df = pd.DataFrame(data)
    #print(df.head())
        
    # Writing dataframe to csv
    df.to_csv(os.path.abspath(os.path.join('data/output/', 'srcML_K9_output_ver3.csv')))
       



# def outPutBuilder(**kwargs):
#     cols = [
#             'fullclasspath', 
#             'methodName',
#             'isPublicMethod',
#             'isPrivateMethod',
#             'isProtectedMethod',
#             'isStaticMethod',
#             'isAbstractMethod',
#             'numParameters'
#         ]
#     rows = []
#     dict = {}

#     for key, value in kwargs.items():
#         key = []
#         dict = key.append(value)
            

#     # fullclasspath = []
#     # methodName = []
#     # isPublicMethod = []
#     # isPrivateMethod = []
#     # isProtectedMethod = []
#     # isAbstractMethod = []
#     # numParameters = []

#     rows.append(dict)
#     df = pd.DataFrame(rows)
    
#     # Writing dataframe to csv
#     df.to_csv(os.path.abspath(os.path.join('data/output/', 'srcML_K9_output.csv')))




def parser(root, ns):

    # getting all classes in the document
    units = root.findall("srcml:unit", ns)
    extractMethods(units, ns)

if __name__ == '__main__':

    file_name = 'srcML_K9.xml'
    input_data = os.path.abspath(os.path.join('data/input', file_name))

    tree = ET.parse(input_data)
    root = tree.getroot()

    # namespace prefix
    ET.register_namespace("srcml", "http://www.srcML.org/srcML/src")
    ns = {"srcml": "http://www.srcML.org/srcML/src"}

    # ET.dump(tree)

    parser(root, ns)