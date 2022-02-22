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
    methodLOC = []

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
                _numParameters = len(methods.findall('srcml:parameter_list/srcml:parameter', ns))


                # split types of parameters
                type_of_params = methods.findall('srcml:parameter_list/srcml:parameter', ns)
                
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

                for type_of_param in type_of_params:
                    if type_of_param is not None:
                        try:
                            if type_of_param.find('srcml:decl/srcml:type/srcml:name', ns).text  == "int":
                                _numIntParams += 1
                            if type_of_param.find('srcml:decl/srcml:type/srcml:name', ns).text  == "String":
                                _numStringParams += 1
                            if type_of_param.find('srcml:decl/srcml:type/srcml:name', ns).text  == "boolean":
                                _numBooleanParams += 1
                            if type_of_param.find('srcml:decl/srcml:type/srcml:name', ns).text  == "byte":
                                _numByteParams += 1
                            if type_of_param.find('srcml:decl/srcml:type/srcml:name', ns).text  == "short":
                                _numShortParams += 1
                            if type_of_param.find('srcml:decl/srcml:type/srcml:name', ns).text  == "long":
                                _numLongParams += 1
                            if type_of_param.find('srcml:decl/srcml:type/srcml:name', ns).text  == "char":
                                _numCharParams += 1
                            if type_of_param.find('srcml:decl/srcml:type/srcml:name', ns).text  == "double":
                                _numDoubleParams += 1
                            if type_of_param.find('srcml:decl/srcml:type/srcml:name', ns).text  == "float":
                                _numFloatParams += 1
                            if type_of_param.find('srcml:decl/srcml:type/srcml:name', ns).text \
                                 not in ['int', 'String', 'boolean', 'byte','short', 'long', 'char', 'double', 'float']:
                                _numObjectParams += 1
                        except:
                            print("error")

                # determine if the method is overriden
                _isOverrideMethod = False
                check_override = methods.find('srcml:annotation/srcml:name', ns)
                
                if check_override is not None and check_override.text == "Override":
                    _isOverrideMethod = True     
                

                # calculate the loc within a method
                method_block = methods.find('srcml:block', ns)
                if method_block is not None:
                    _methodLOC = len(method_block)
                    # print(_methodLOC)

                        
                        



                
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
                methodLOC.append(_methodLOC)

    cols = [
            'fullclasspath',
            'className', 
            'isInnnerClass',
            'methodName', 
            'isPublicMethod',
            'isPrivateMethod',
            'isProtectedMethod', 
            'isStaticMethod',
            'isAbstractMethod',
            'returnType',
            'numParameters',
            'numIntParams',
            'numStringParams',
            'numBooleanParams',
            'numByteParams',
            'numShortParams',
            'numLongParams',
            'numCharParams',
            'numDoubleParams',
            'numFloatParams',
            'numObjectParams',
            'isOverrideMethod',
            'methodLOC'
        ]
    

    rows = {
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
            'numStringParams': numIntParams,
            'numBooleanParams': numBooleanParams,
            'numByteParams': numByteParams,
            'numShortParams': numShortParams,
            'numLongParams': numLongParams,
            'numCharParams': numCharParams,
            'numDoubleParams': numDoubleParams,
            'numFloatParams': numFloatParams,
            'numObjectParams': numObjectParams,
            'isOverrideMethod': isOverrideMethod,
            'methodLOC': methodLOC
    }

    df = pd.DataFrame(rows)
        
    # Writing dataframe to csv
    df.to_csv(os.path.abspath(os.path.join('data/output/', 'srcML_K9_output_ver2.csv')))
       



def outPutBuilder(**kwargs):
    cols = [
            'fullclasspath', 
            'methodName',
            'isPublicMethod',
            'isPrivateMethod',
            'isProtectedMethod',
            'isStaticMethod',
            'isAbstractMethod',
            'numParameters'
        ]
    rows = []
    dict = {}

    for key, value in kwargs.items():
        key = []
        dict = key.append(value)
            

    # fullclasspath = []
    # methodName = []
    # isPublicMethod = []
    # isPrivateMethod = []
    # isProtectedMethod = []
    # isAbstractMethod = []
    # numParameters = []

    rows.append(dict)
    df = pd.DataFrame(rows)
    
    # Writing dataframe to csv
    df.to_csv(os.path.abspath(os.path.join('data/output/', 'srcML_K9_output.csv')))




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