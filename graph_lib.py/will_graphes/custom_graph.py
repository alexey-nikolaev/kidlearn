#!/usr/bin/python
# -*- coding: latin-1 -*-

import matplotlib.pyplot as plt
import time
import numpy as np
import pickle
import copy

def load_graph(filename):
	with open(filename, 'rb') as fichier:
		mon_depickler=pickle.Unpickler(fichier)
		tempgr=mon_depickler.load()
	return tempgr


class CustomGraph(object):
	def __init__(self,Y,*arg,**kwargs):
		self.keepwinopen=0
		self.sort=1
		self.filename="graph"+time.strftime("%Y%m%d%H%M%S", time.localtime())
		if "filename" in kwargs.keys():
			self.filename=kwargs["filename"]
		self.title=self.filename
		self.xlabel="X"
		self.ylabel="Y"
		self.alpha=0.3

		self.Yoptions=[{}]

		self.xmin=[0,0]
		self.xmax=[0,5]
		self.ymin=[0,0]
		self.ymax=[0,5]
		
		self.std=0
		
		self._Y=[Y]
		self.stdvec=[0]*len(Y)

		if len(arg)!=0:
			self._X=[Y]
			self._Y=[arg[0]]
		else:
			self._X=[range(0,len(Y))]


		self.extensions=["eps","png"]

		for key,value in kwargs.iteritems():
			setattr(self,key,value)

		self.stdvec=[self.stdvec]

		if not isinstance(self.xmin,list):
			temp=self.xmin
			self.xmin=[1,temp]
		if not isinstance(self.xmax,list):
			temp=self.xmax
			self.xmax=[1,temp]
		if not isinstance(self.ymin,list):
			temp=self.ymin
			self.ymin=[1,temp]
		if not isinstance(self.ymax,list):
			temp=self.ymax
			self.ymax=[1,temp]


	def show(self):
		plt.figure()
		plt.ion()
		self.draw()
		plt.show()

	def save(self,*path):
		if len(path)!=0:
			out_path=path[0]
		else:
			out_path=""
		with open(out_path+self.filename+".b", 'wb') as fichier:
			mon_pickler=pickle.Pickler(fichier)
			mon_pickler.dump(self)

	def write_files(self,*path):
		if len(path)!=0:
			out_path=path[0]
		else:
			out_path=""

		self.draw()
		self.save(out_path)
		for extension in self.extensions:
			plt.savefig(out_path+self.filename+"."+extension,format=extension)


	def draw(self):
		colormap=['blue','red','green','black','yellow','cyan','magenta']
		#plt.figure()
		plt.ion()
		plt.cla()
		plt.clf()
		for i in range(0,len(self._Y)): 

			Xtemp=self._X[i]
			Ytemp=self._Y[i]
			if self.sort:
				tempdic={}
				for j in range(0,len(Xtemp)):
					tempdic[Xtemp[j]]=Ytemp[j]
				temptup=sorted(tempdic.items())
				for j in range(0,len(temptup)):
					Xtemp[j]=temptup[j][0]
					Ytemp[j]=temptup[j][1]

			Xtemp=self._X[i]
			stdtemp=self.stdvec[i]
			if self.sort:
				tempdic={}
				for j in range(0,len(Xtemp)):
					tempdic[Xtemp[j]]=stdtemp[j]
				temptup=sorted(tempdic.items())
				for j in range(0,len(temptup)):
					Xtemp[j]=temptup[j][0]
					stdtemp[j]=temptup[j][1]
			if self.std:
				Ytempmin=[0]*len(Ytemp)
				Ytempmax=[0]*len(Ytemp)
				for j in range(0,len(Ytemp)):
					Ytempmax[j]=Ytemp[j]+stdtemp[j]
					Ytempmin[j]=Ytemp[j]-stdtemp[j]
				plt.fill_between(Xtemp,Ytempmin,Ytempmax,alpha=self.alpha,color=colormap[i%7],**self.Yoptions[i])
			plt.plot(Xtemp,Ytemp,color=colormap[i%7],**self.Yoptions[i])
		plt.xlabel(self.xlabel)
		plt.ylabel(self.ylabel)
		plt.title(self.title)

		if self.xmin[0]:
			plt.xlim(xmin=self.xmin[1])
		if self.xmax[0]:
			plt.xlim(xmax=self.xmax[1])
		if self.ymin[0]:
			plt.ylim(ymin=self.ymin[1])
		if self.ymax[0]:
			plt.ylim(ymax=self.ymax[1])
		plt.legend()
		plt.draw()


	def add_graph(self,other_graph):
		self._X=self._X+other_graph._X
		self._Y=self._Y+other_graph._Y
		self.Yoptions=self.Yoptions+other_graph.Yoptions
		self.stdvec=self.stdvec+other_graph.stdvec

	def merge(self):
		Yarray=np.array(self._Y)
		stdarray=np.array(self.stdvec)
		stdtemp=[]
		Ytemp=[]
		self.Yoptions=[self.Yoptions[0]]

		for i in range(0,len(self._Y[0])):
			Ytemp.append(np.mean(list(Yarray[:,i])))
			stdtemp.append(np.std(list(Yarray[:,i])))
		self._Y=[Ytemp]
		self.stdvec=[stdtemp]
		self._X=[self._X[0]]


	def wise_merge(self):
		param_list=[]
		for i in range(len(self.Yoptions)):
			param_list.append(self.Yoptions[i]["label"])
		param_values={}
		for ind,param in enumerate(param_list):
			if param not in param_values.keys():
				param_values[param]=copy.deepcopy(self)
				param_values[param]._X=[self._X[ind]]
				param_values[param]._Y=[self._Y[ind]]
				param_values[param].Yoptions=[self.Yoptions[ind]]
			else:
				tempgraph=copy.deepcopy(self)
				tempgraph._X=[self._X[ind]]
				tempgraph._Y=[self._Y[ind]]
				tempgraph.Yoptions=[self.Yoptions[ind]]
				param_values[param].add_graph(copy.deepcopy(tempgraph))
		tempgraph=copy.deepcopy(self)
		tempgraph._X=[]
		tempgraph._Y=[]
		tempgraph.Yoptions=[]
		tempgraph.stdvec=[]
		for key in param_values.keys():
			param_values[key].merge()
			tempgraph.add_graph(param_values[key])
		return tempgraph

	def empty(self):
		self._Y=[]
		self._X=[]
		self.Yoptions=[]
		self.stdvec=[]


