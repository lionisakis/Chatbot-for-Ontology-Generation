from cgitb import reset
from re import sub
import modules.chatbotTalks as talk
import modules.ontologyManager as manager
import modules.chatbotHears as hear
import modules.searchOntology as search
import modules.utility as utility

def checkInheritance(word,parent,ui):
    # check if there is a parent to check for the inheritance
    if parent == None:
        return -1

    # check if the inheritance is correct
    answer=utility.questionWithYesOrNo(ui,talk.ontoCheck(parent,word))
    
    # there is a parent and there is wrong with the inheritance
    if answer==0:        
        # check IDENTITY
        answer=utility.questionWithYesOrNo(ui,talk.identityComponentOf(parent,word))
        if answer==1:
            return 1
        else:
            ui.rememberOneTime("Ok now something new.\n")
            answer=utility.questionWithYesOrNo(ui,talk.identityComponentOf(word,parent))
            if answer==1:
                return 2
            else:
                # check UNITY
                answer=utility.questionWithYesOrNo(ui,talk.unityComposedOf(parent,word))
                if answer==1:
                    return 3
                else:
                    ui.rememberOneTime("Ok now something new.\n")
                    answer=utility.questionWithYesOrNo(ui,talk.unityComposedOf(word,parent))
                    if answer==1:
                        return 4
                    else:    
                        ui.rememberOneTime("I cannot understand how the connection goes so I will not use this connection.\n")
                        ui.rememberOneTime("Please fix the connection between \""+parent+"\" - \""+word+"\"")
                        return 5
    else:
        return 0

def addInheritance(noun,parent,data,ui):
    # so check for the inheritance
    keepParent=[]
    keepRelation=[]
    if parent!=None:
        for theParent in parent:
            result=checkInheritance(noun,theParent,ui)
            if result==0:
                keepParent.append(theParent)
            elif result==1:
                relation=theParent.title()+"_ComponentOf_"+noun.title()
                keepRelation.append((relation,theParent,noun))
            elif result==2:
                relation=noun.title()+"_ComponentOf_"+theParent.title()
                keepRelation.append((relation,noun,theParent))
            elif result==3:
                relation=theParent.title()+"_ComposedOf_"+noun.title()
                keepRelation.append((relation,theParent,noun))                
            elif result==4:
                relation=noun.title()+"_ComposedOf_"+theParent.title()
                keepRelation.append((relation,noun,theParent))
    
    # add parents
    for theParent in keepParent:        
        manager.addParent(data[2],data[0][noun][0],data[0][theParent][0],ui)
        data[0][noun][2].append(theParent)

    # add relations
    for relation,object1,object2 in keepRelation:
        createRelation(data,ui,object1,relation,object2)

    return True

def createNoun(noun,parent,ui,moreGeneralized=True):
    ui.moreGeneralized=moreGeneralized
    # check if the word is in data base
    for word in ui.data[0].keys():
        if noun.lower()==word.lower():
            ui.rememberOneTime("The word \""+noun+"\" is already in the dataBase\n")
            ui.taskNouns-=1
            ui.checkTask()
            return 
    # so check for the inheritance
    # keepParent=[]
    # keepRelation=[]
    # if parent!=None:
    #     for theParent in parent:
    #         result=checkInheritance(noun,theParent,ui)
    #         if result==0:
    #             keepParent.append(theParent)
    #         elif result==1:
    #             relation=theParent.title()+"_ComponentOf_"+noun.title()
    #             keepRelation.append((relation,theParent,noun))
    #         elif result==2:
    #             relation=noun.title()+"_ComponentOf_"+theParent.title()
    #             keepRelation.append((relation,noun,theParent))
    #         elif result==3:
    #             relation=theParent.title()+"_ComposedOf_"+noun.title()
    #             keepRelation.append((relation,theParent,noun))                
    #         elif result==4:
    #             relation=noun.title()+"_ComposedOf_"+theParent.title()
    #             keepRelation.append((relation,noun,theParent))

    ui.search()


def createRelation(data,ui,obj1,relation,obj2):
    # mark as used
    data[0][obj1][3]=1
    data[0][obj2][3]=1

    if relation not in data[1].keys():
        # create the relationship
        data[1][relation]=[manager.ConnectObjects(data[2],relation,data[0][obj1][0],data[0][obj2][0],ui),[obj1],relation,obj2]
        ui.AddToTableRelationship(obj1,relation,obj2)
    else:
        manager.AddConnection(data[2],data[1][relation][0],data[0][obj1][0],ui)
        data[1][relation][1].append(obj1)
        ui.AddToTableRelationship(data[1][relation][0],relation,data[1][relation][1][-1])

