#!/usr/bin/env python
# coding: utf-8

# In[1]:


root=None
sum=0
sort_q=[]
import random
import sys


# In[2]:


class PlayerNode:
    def __init__(self, Pid):
        self.PId = Pid
        self.attrCtr = 1
        self.left = None
        self.right = None
    
    def insert_player(self, Pid):
        '''
        insert player_id at first available empty slot O(n) (balanced tree)
        '''
        tb_queue=[]
        tb_queue.append(self)
        while(True):
            if len(tb_queue)==0:
                break
            comp_obj=tb_queue[0]
            tb_queue.pop(0)
            if comp_obj.left is None:
                comp_obj.left=PlayerNode(Pid)
                break
            else:
                tb_queue.append(comp_obj.left)
            if comp_obj.right is None:
                comp_obj.right=PlayerNode(Pid)
                break
            else:
                tb_queue.append(comp_obj.right)
                
    def insert_player_imbalanced(self, Pid):
        '''
        insert player_id at root O(1)
        '''
        global root
        temp=root
        root=PlayerNode(Pid)
        if random.randint(0,1)==0:
            root.left=temp
        else:
            root.right=temp
        
                
    def _recordSwipeRec(self, pNode, Pid):
        if pNode is None:
            return None
        if pNode.PId==Pid:
            pNode.attrCtr+=1
            return pNode
        ret_node=pNode._recordSwipeRec(pNode.left,Pid)
        if ret_node:
            return ret_node
        ret_node=pNode._recordSwipeRec(pNode.right,Pid)
        if ret_node:
            return ret_node
        if pNode==root:
            pNode.insert_player_imbalanced(Pid)
            
    def _getSwipeRec(self, pNode):
        global sum
        if pNode==root:
            sum=0
        if pNode is None:
            return 0
        else:
            sum=sum+1
            pNode._getSwipeRec(pNode.left)
            pNode._getSwipeRec(pNode.right)
        if pNode==root:
            with open('outputPS10Q1.txt', 'w') as f:
                f.write("Total number of players recorded today: {}".format(sum))
        
    def _onPremisesRec(self, pNode):
        global sum
        if pNode==root:
            sum=0
        if pNode is None:
            return 0
        else:
            if pNode.attrCtr%2==1:
                sum=sum+1
            pNode._onPremisesRec(pNode.left)
            pNode._onPremisesRec(pNode.right)
        if pNode==root:
            with open('outputPS10Q1.txt', 'a') as f:
                if sum==0:
                    f.write("\nNo players present on premises.")
                else:
                    f.write("\n{} players still on premises.".format(sum))
                    
    def _checkEmpRec(self, pNode, EId):
        if pNode:
            if pNode.PId==EId:
                with open('outputPS10Q1.txt', 'a') as f:
                    if pNode.attrCtr%2==1:
                        f.write("\nPlayer id {} swiped {} times today and is currently in hotel".format(pNode.PId,pNode.attrCtr))
                    else:
                        f.write("\nPlayer id {} swiped {} times today and is currently outside hotel".format(pNode.PId,pNode.attrCtr))
                return pNode
            ret_node=pNode._checkEmpRec(pNode.left,EId)
            if ret_node:
                return ret_node
            ret_node=pNode._checkEmpRec(pNode.right,EId)
            if ret_node:
                return ret_node
            if pNode==root:
                with open('outputPS10Q1.txt', 'a') as f:
                    f.write("\nPlayer id {} did not swipe today.".format(EId))
    
    def _frequentVisitorRec(self, pNode, frequency):
        if pNode==root:
            with open('outputPS10Q1.txt', 'a') as f:
                    f.write("\nPlayers that swiped more than {} number of times today are:".format(frequency))
        if pNode:
            if pNode.attrCtr>=frequency:
                with open('outputPS10Q1.txt', 'a') as f:
                    f.write("\n{}, {}".format(pNode.PId,pNode.attrCtr))
            pNode._frequentVisitorRec(pNode.left,frequency)
            pNode._frequentVisitorRec(pNode.right,frequency)
                        
    def printRangePresent_unsorted(self, StartId, EndId):                             #O(n) for unsorted output
        if self==root:
            with open('outputPS10Q1.txt', 'a') as f:
                f.write("\nRange: {} to {}\nPlayer swipe:".format(StartId,EndId))
        if self:
            if self.left:                                        #Inorder traversal left->Root->Right
                self.left.printRangePresent_unsorted(StartId, EndId)
            if self.PId>=StartId and self.PId<=EndId:
                state="in" if self.attrCtr%2==1 else "out"
                with open('outputPS10Q1.txt', 'a') as f:
                    f.write("\n{}, {}, {}".format(self.PId,self.attrCtr,state))
            if self.right:
                self.right.printRangePresent_unsorted(StartId, EndId)
                
    
    def printRangePresent(self, StartId, EndId):                                      #O(nlogn) for sorted output
        global sort_q
        if self==root:
            with open('outputPS10Q1.txt', 'a') as f:
                    f.write("\nRange: {} to {}\nPlayer swipe:".format(StartId,EndId))
        if self:
            if self.left:                                                         #Inorder traversal left->Root->Right
                self.left.printRangePresent(StartId, EndId)
            if self.PId>=StartId and self.PId<=EndId:
                state="in" if self.attrCtr%2==1 else "out"
                sort_q.append((self,state))
            if self.right:
                self.right.printRangePresent(StartId, EndId)
            if self==root:
                sort_q= sorted(sort_q,key=lambda x: (x[0].PId))
                with open('outputPS10Q1.txt', 'a') as f:
                    for i in sort_q:
                        f.write("\n{}, {}, {}".format(i[0].PId,i[0].attrCtr,i[1]))


# In[3]:


def trigger_function():
    global root
    global sum
    try: 
        input_file=open("./inputPS10Q1.txt","r")
    except:
        print('Please ensure the input file has the correct name(inputPS10Q1.txt) and present in current working directory')
        sys.exit()
    list_i=input_file.readlines()
    list_i=[i for i in map(int, list_i)]
    #root=PlayerNode(30)
    if root==None:
        root=PlayerNode(list_i[0])
    else:
        root._recordSwipeRec(root, list_i[0])
    for i in range(1,len(list_i),1):
        root._recordSwipeRec(root, list_i[i])
    sum=0
    root._getSwipeRec(root)
    try:
        prompt_file=open("./promptsPS10Q1.txt","r")
    except:
        print('Please ensure the Prompts file has the correct name(promptsPS10Q1.txt) and present in current working directory')
        sys.exit()
    list_p=prompt_file.readlines()
    for i in range(0,len(list_p),1):
        if list_p[i].split(':')[0]=="onPremises":
            sum=0
            root._onPremisesRec(root)
        if list_p[i].split(':')[0]=="checkPlay":
            pid=int(list_p[i].split(':')[1])
            root._checkEmpRec(root,pid)
        if list_p[i].split(':')[0]=="freqVisit":
            frequency=int(list_p[i].split(':')[1])
            freq_list=[]
            root._frequentVisitorRec(root,frequency)
        if list_p[i].split(':')[0]=="range":
            StartId=int(list_p[i].split(':')[1])
            EndId=int(list_p[i].split(':')[2])
            root.printRangePresent(StartId,EndId)


# In[4]:


if __name__ == "__main__":
    trigger_function()

