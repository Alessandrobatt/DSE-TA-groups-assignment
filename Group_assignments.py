from math import nan
import itertools

##############################
# USER INPUTS
##############################

# TA preferences, each list must end in nan to mark the end of the preferences
# preferences = {
#     "Alessandro":[27, 25, 24, 26, 15, 7, 9, 22, 19, 14, nan],
#     "Austin":[26, 27, 15, 24, 22, 25, 23, 4, 1, 28, nan],
#     "Crina":[26, 22, 15, 28, 23, nan],
#     "Kim":[22, 23, 24, 25, 9, 16, 19, 11, 27, 1, nan],
#     "Koen":[11, 9, 16, 4, 29, nan],
#     "Yaren":[5, 11, 12, 18, 29, 10, 3, 9, 2, 6, nan],
#     "Praj":[21, 29, 18, 19, 13, nan],
#     "Korneel":[7, 3, 29, 17, 16, 9, nan]
# }

preferences = {
    "Momo":[25, 23, 4, 24, 21, 20, 18, 22, 3, 5, nan],
    "Crina":[24, 30, 29, 14, 12, 22, 23, 20, 2, 21, nan],
    "Katharina":[21, 2, 15, 18, 20, 30, 23, 22, 24, 8, nan],
    "Igor":[28, 9, 13, 26, 19, 30, 15, 27, 12, 4, nan],
    "Marco":[18, 25, 9, 20, 23, 21, 2, 30, 1, 6, nan],
    "Marianna":[9, 13, 12, 4, 28, 14, 3, 1, 26, 7, nan],
    "Farouk":[24, 10, 30, 1, 23, 21, 30, 19, 4, 20, nan],
    "Kiva":[31, 19, 8, 5, 20, 7, 10, 15, 12, 22, nan]
}

# Names of all TAs
# names = ["Alessandro", "Austin", "Crina", "Kim", "Koen", "Yaren", "Praj", "Korneel"]
names = ["Momo", "Crina", "Katharina", "Igor", "Marco", "Marianna", "Farouk", "Kiva"]

# how much each person cares about their preference, [1] if they care, [0] if they don't, and anything in between
relevance = [1, 1, 1, 1, 1, 1, 1, 1]

# how many groups would each like to have
# desired_number_of_groups = [3, nan, 3, 4, nan, 4, nan, nan]     # (provided)
desired_number_of_groups_temp = [4, nan, 3, 4, nan, 4, nan, 4]     # (provided)
desired_number_of_groups = [4, 4, 3, 4, 3, 4, 4, 4]             # (fill out based on preferences above)

# groups available to be assigned
groups = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]


##############################
# ASSIGNMENT ALGORITHM
##############################

# generate all possible combinations of numbers 0 through 7 --> every permutation will be a starting order to pick
# groups
start_orders_lst = list(itertools.permutations(range(8)))
print(f"\nPossible pick order permutations: {len(start_orders_lst)}")


# num_groups = groups[-1]
# max_per_TA = 1
# assigned_groups = sum(desired_number_of_groups)
#
# while assigned_groups < num_groups:
#     for ta_idx in range(len(names)):
#         if desired_number_of_groups[ta_idx] < max_per_TA:
#             desired_number_of_groups[ta_idx] += 1
#             max_per_TA = max(desired_number_of_groups)
#
#     assigned_groups = sum(desired_number_of_groups)


# # filling out remaning group preferences
# num_four_ta = desired_number_of_groups.count(4)
# for i, preferred_num_groups in enumerate(desired_number_of_groups):
#     if preferred_num_groups is nan:
#         if num_four_ta < 5:
#             desired_number_of_groups[i] = 4
#         else:
#             desired_number_of_groups[i] = 3
#     num_four_ta = desired_number_of_groups.count(4)

print(f"Number of groups for each TA: {desired_number_of_groups}")

# calculate the loss for a given set of assigned groups and a list of groups to be assigned
def loss(assigned, groups_nums_ext):

    loss_lst = []   # loss for each person

    groups = []
    # check that all the grops in the list "groups" were indeed assigned to people
    for name in names:
        for group in assigned[name]:
            groups.append(group)

    # now we have a list of all the assigned groups, first remove the "nan" in the list, placeholders for people with
    # only 3 groups
    while nan in groups:
        groups.remove(nan)

    # sort both groups to make sure they can safely be compared
    groups.sort()
    groups_nums_ext.sort()

    # check that the assigned groups are the same as the provided groups list ("groups_nums_ext")
    if groups != groups_nums_ext:
        raise Exception(f"\n{'_'*50}\nGroups not correctly assigned, 'groups' list does not match with 'assigned' dictionary")


    # now that we know all groups have been assigned correctly, for each TA, check how
    # far from their preferences the solution is

    # loop through every TA name
    for name_idx, name in enumerate(names):

        # print(f"\n\n{name}")

        # loss for this person
        loss = 0

        # get their preferences and assigned groups
        goal = preferences[name]
        received = assigned[name]

        # loop through each assigned group
        for i, group_num in enumerate(received):

            # check that the assigned group is not nan, if it is, then move to the next name
            if group_num is nan:
                break

            # get the index of this group on their preference list
            # first check that the assigned group was even in the preferences, else add 10 to the loss
            if group_num in goal:
                goal_idx = goal.index(group_num)

                # find the difference to the index in the preference list and use that as a loss
                # divide by the goal index, if high on preference list, larger loss for same difference in order
                loss += (goal_idx - i) / (goal_idx + 1)
            else:
                loss += 10
        # print(f"preferences: {goal}")
        # print(f"received groups: {received}")
        # print(loss)

        # scale the loss for this person by how much the care about their preferences
        loss_lst.append(loss * relevance[name_idx])

    # print(f"\nLoss list containing loss number for every TA: {loss_lst}\n\n")
    return loss_lst

# loss(assigned, [1, 3, 4, 2])

# initialise a loss and assigned list for every possible pick_order
loss_lst = []
assigned_lst = []


# check that the preferred number of groups per TA actually add up to the number of available groups
if sum(desired_number_of_groups) != len(groups):
    raise Exception("Desired number of groups per TA do not add up to the number of available groups")


# loop through every starting order list
for i, pick_order in enumerate(start_orders_lst):
    # if i > 0:
    #     break

    # print(f"\n\nPick order from the 'names' list: {list(pick_order)}")

    # create a new list of groups still to be assigned, remove from here as groups are assigned to TAs
    groups_to_be_assigned = groups[:]

    # create a new empty assigned dictionary
    assigned = {
        "Momo":         [],
        "Crina":        [],
        "Katharina":    [],
        "Igor":         [],
        "Marco":        [],
        "Marianna":     [],
        "Farouk":       [],
        "Kiva":         []
    }

    # in the order provided by the "pick_order" list, loop through the TA names
    # wrap that in a while loop until the "groups_to_be_assigned" list is empty

    # initialise the skip_name flags for all names to False
    skip_name = [False, False, False, False, False, False, False, False]

    while len(groups_to_be_assigned) > 0:

        for name_idx in pick_order:
            name = names[name_idx]
            # print(name)

            # check that this name is not one which ran out of preferences, if so, skip it directly
            if skip_name[name_idx]:
                continue

            # loop through preferences and stop when one is found which is still in the groups to be assigned
            for preference in preferences[name]:
                # check that it is still in the groups to be assigned
                if preference in groups_to_be_assigned:
                    break   # break out of the loop to confirm this preference

                # else if preference is nan, set the skip TA flag to true so others with preferences can have priority
                elif preference is nan:
                    skip_name[name_idx] = True
                    break
                # else move to the next preference and repeat
                # every preference list ends in nan, so if not preference available is found, the person is just skipped

            # check how many names have already been assigned to this TA, of 4 or more, set the skip flag to True
            assigned_groups_num = len(assigned[name])
            if assigned_groups_num >= desired_number_of_groups[name_idx]:
                skip_name[name_idx] = True

            if skip_name[name_idx]:
                continue

            # add this preference to the assigned groups for this TA
            assigned[name].append(preference)

            # remove the group number from groups to be assigned
            groups_to_be_assigned.remove(preference)

        # now that we have gone through all the names again, check that there are still names which are not to be skipped
        # if all names are to be skipped, assign the remaining groups in the pick_order
        # print(f"\n{skip_name}\n")
        if skip_name.count(True) == len(skip_name):      # if all names have the flag raised to skip
            # go in the pick order once again

            # reset the skip_name flags
            skip_name = [False, False, False, False, False, False, False, False]

            # check how many groups were assigned to each TA

            while len(groups_to_be_assigned) > 0:

                # list with number of assigned groups per name
                num_groups_assigned = [len(assigned[ass_name]) for ass_name in assigned]
                # print(num_groups_assigned)

                # pick the name with the lowest number of assigned groups
                name_idx_lst = [i for i, x in enumerate(num_groups_assigned) if x == min(num_groups_assigned)]
                # check that this name does not have the skip flag up already
                # it is to skip, pic the next with the lowest number of assigned groups
                for name_idx in name_idx_lst:
                    if not skip_name[name_idx]:
                        break
                name = names[name_idx]


                # check that that name has not 4 or more groups already, if so, raise the skip flag
                if len(assigned[name]) >= desired_number_of_groups[name_idx]:
                    skip_name[name_idx] = True

                # skip names which have the skip_name flag raise
                if skip_name[name_idx]:
                    continue

                # otherwise, assign this TA the first group in the remaining groups list.
                # Check that there are actually groups left!
                if len(groups_to_be_assigned) > 0:
                    assigned[name].append(groups_to_be_assigned[0])
                    groups_to_be_assigned.pop(0)
                # print(f"\n{skip_name}\n")

        # finished assigning names!

    # for ass_name in assigned:
    #     print(assigned[ass_name])


    # calculate loss for this particular assignment

    loss_lst.append(sum(loss(assigned, groups)))
    assigned_lst.append(assigned)

# print(loss_lst)
best_idx = loss_lst.index(min(loss_lst))

assigned = assigned_lst[best_idx]
print(f"Best picking order permutation index: {best_idx}")
print(f"\nAssigned groups for each TA:")
for assigned_name in assigned:
    print(f"{assigned_name}: {assigned[assigned_name]}")