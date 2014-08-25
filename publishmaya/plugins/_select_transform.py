import publish.config
import publish.backend.plugin

import maya.cmds as cmds


class SelectTransform(publish.backend.plugin.Selector):
    """Select instances of node-type 'transform'

    Opens up the doors for nested instances.

    E.g.          -> /root/characters_GRP/MyCharacter.publishable
    As opposed to -> /root/MyCharacter.publishable

    But lacks ability to append non-DAG nodes.

    E.g.          -> /root/MyCharacter.publishable/an_object_set

    """

    hosts = ['maya']
    version = (0, 1, 0)

    def process(self, context):
        for transform in cmds.ls("*." + publish.config.identifier,
                                 objectsOnly=True,
                                 type='transform'):

            instance = publish.backend.plugin.Instance(name=transform)

            instance.add(transform)
            for child in cmds.listRelatives(transform, allDescendents=True):
                    instance.add(child)

            attrs = cmds.listAttr(transform, userDefined=True)
            for attr in attrs:
                if attr == publish.config.identifier:
                    continue

                try:
                    value = cmds.getAttr(transform + "." + attr)
                except:
                    continue

                instance.config[attr] = value

            context.add(instance)

            yield instance, None
