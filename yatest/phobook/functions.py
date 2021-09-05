def moderators_lists(queryset):
    moderators_list = []
    if queryset.exists():
        for query in queryset:
            moderators_list.append(query[2])
    return moderators_list
