#!/usr/bin/python

"""
Based on an example from https://github.com/CognitiveAtlas/cogat-python
    by Vanessa Sochat
"""
try:
    from cognitiveatlas.api import get_concept, get_task
except:
    pass


    

# EXAMPLE 1: #########################################################
# We are going to retrieve all cognitive paradgims (tasks), find 
# associated contrasts, and then find the cognitive concepts 
# the contrasts are asserted to measure. You can choose to do these 
# calls and arrange the data in whatever format fits your needs
######################################################################

# Step 1: Retrieve all tasks. When we do a general call for all tasks, we 
# actually only retrieve the basic information:
#
# [u'def_id_user',
# u'id',
# u'definition_text',
# u'event_stamp',
# u'def_event_stamp',
# u'concept_class',
# u'def_id',
# u'id_concept_class',
# u'id_user',
# u'name',
# u'type',
# u'alias']

#
# We will need a second call to get the rest, the addition of:
#[u'conclass',
# u'implementations',
# u'disorders',
# u'discussion',
# u'indicators',
# u'conditions',
# u'contrasts',
# u'external_datasets',
# u'umarkdef',
# u'umark',
# u'history']

# Step 2: Find contrasts associated with each task
# Note that this is an inefficient way to retrieve the full data, but it will work!
if __name__ == '__main__':
    task_uids = [task["id"] for task in get_task().json]
    contrasts = dict() # contrast lookup by task uid

    # Now we can retrieve the full data. We are interested in contrasts, so let's save those.
    for t, task in enumerate(task_uids):
        if task not in contrasts:
            print('Task {} of {}'.format(t, len(task_uids)))
            task_complete = get_task(task).json[0]
            # Only save if we have contrasts
            if len(task_complete["contrasts"]) > 0:
                contrasts[task] = task_complete["contrasts"]

    # How many tasks have contrasts?
    print('# contrasts: {}'.format(len(contrasts)))
    # 437

    # Step 3: Make a contrast --> concept lookup
    concepts = dict()
    for t, taskContrasts in enumerate(contrasts.items()):
        task_uid, contrast_set = taskContrasts
        print('Task {} of {}'.format(t, len(task_uids)))
        for contrast in contrast_set:
            contrast_uid = contrast["id"]
            if contrast_uid not in concepts:
                try: # Some calls don't work
                    concepts[contrast_uid] = get_concept(contrast_id=contrast_uid).json[0]
                except:
                    pass

    # How many concepts are asserted to measure different contrasts?
    len(concepts)
    print('# concepts: {}'.format(len(concepts)))

    allcontrasts = []
    for tid, taskContrasts in contrasts.items():
        for contrast in taskContrasts:
            allcontrasts.append(contrast)

    get_concept().pandas.to_csv('data/concepts.csv', encoding='utf-8')
    pandas.DataFrame(allcontrasts).to_csv('data/contrasts.csv', encoding='utf-8')
    pickle.dump(concepts, open('data/conceptsByContrasts.pickle','wb'))


