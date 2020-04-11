import hou

Name = "Bone"
Nodes = hou.selectedNodes()

if len(Nodes) >= 2:

    netparent = Nodes[0].node("..")
    parent = netparent.createNode("null",node_name=Name + "_Root")
    prefix = Name + "_"
     
    item_to_become_input = parent
    boneList = []

    for i, Node in enumerate(Nodes[:-1]):
        # ボーンを作成
        Bone = netparent.createNode("bone",node_name="IK_bone" + str(i+1))

        # 位置合わせ
        xform = Node.worldTransform()
        Bone.setWorldTransform(xform)
        
        # rootの位置合わせ
        if i == 0:
            parent.setWorldTransform(xform)
            
        #　Keep Position
        Bone.setParms({"keeppos":True})

        #　Boneの長さを調整

        nb_xform = Nodes[i+1].worldTransform()
        vector = nb_xform.extractTranslates() - xform.extractTranslates()
        l = vector.length()
        Bone.setParms({"length": l})

        #　Boneを回転
        rootVector = hou.Vector3([0.0, 0.0, -1.0])

        nVector = vector.normalized()
        m = rootVector.matrixToRotateTo(nVector)
        Rot = m.extractRotates() 
        
        Bone.setParms({"rx":Rot[0]})
        Bone.setParms({"ry":Rot[1]})
        Bone.setParms({"rz":Rot[2]})
        
        #　値を0に            
        Bone.parm("pre_xform").set(0)
        Bone.parm("pre_xform").pressButton()
        
        
        Bone.parm("tx").lock(True)
        Bone.parm("ty").lock(True)
        Bone.parm("tz").lock(True)
        
        
        #　Bone同士を接続する。
        Bone.setInput(0,item_to_become_input)
        item_to_become_input = Bone

        boneList.append(Bone)