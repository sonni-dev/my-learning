# Event-specific payload params for feed
"""

event_schema = {
    'EventType': {
        'action': '',
        'refs': {
            # Any event-specific data points
            'ref_type': 'branch',
            'obj_no': 217,
        },
        'action_str': f'String for feed',
    },
}
"""



event_dict = {
    'CommitCommentEvent': {
        'action': "i['payload']['action']",  # created
        'refs': {},
        'action_str': f"{actor} {action} Commit Comment | Repo: {repo}",
    },
    'CreateEvent': {
        'action': "Created",
        'refs': {
            'ref_type': "i['payload']['ref_type']", # branch, tag, repository
        },
        'action_str': f'Created {ref_type} | Repo: {repo}',
    },
    'DeleteEvent': {
        'action': "Deleted",
        'refs': {
            'ref_type': "i['payload']['ref_type']", # branch, tag
        },
        'action_str': f'Deleted {ref_type} in {repo}',
    },
    'DiscussionEvent': {
        'action': "i['payload']['action']",  # created
        'refs': {
            'ref_type': 'Discussion',
            'obj_name': "i['payload']['discussion']",
        },
        'action_str': f"{actor} {action} {ref_type}: {obj_name}",
    },
    'ForkEvent': {
        'action': "i['payload']['action']",  # forked
        'refs': {
            'ref_type': 'Repository',
            'obj_name': "i['payload']['forkee']",
        },
        'action_str': f"{actor} {action} {ref_type}: {obj_name}",
    },
    'GollumEvent': {
        'action': "Created/Updated",  # General without looping through each page
        'refs': {
            'ref_type': 'Wiki Page(s)',
            'obj_no': "len(i['payload']['pages'])",
        },
        'action_str': f"{action} {obj_no} {ref_type} | Repo: {repo}",
    },
    'IssueCommentEvent': {
        'action': "i['payload']['action']",  # created
        'refs': {
            'ref_type': 'Issue',
            'obj_no': "i['payload']['issue']['number']",
            'obj_name': "i['payload']['issue']['title']",
        },
        'action_str': f"New comment on Issue: #{obj_no}",
    },
    'IssuesEvent': {
        'action': "i['payload']['action']",  # closed, labeled, opened, assigned, reopened
        'refs': {
            'ref_type': 'Issue',
            'obj_no': "i['payload']['issue']['number']",
            'obj_name': "i['payload']['issue']['title']",
            # Only present if assigned is action
            # 'assignee': "i['payload']['assignee']['login']" or "",
            # 'assignees_list': "i['payload']['assignees']" or [],
            # 'assignees': [x.login for x in assignees_list] if assignees_list else [],
            # 'no_assignees': len(assignees_list) or 0,
        },
        'action_str': f"{action} | Issue: #{obj_no}",
    },
    'MemberEvent': {
        'action': "i['payload']['action']",  # added if user accepted invite to repo
        'refs': {
            'ref_type': 'User',
            'obj_name': "i['payload']['member']",
        },
        'action_str': f"{action} {ref_type}: {obj_name} | Repo: {repo}",
    },
    'PublicEvent': {
        'action': "Made Public",
        'refs': {},
        'action_str': f"{action} | Repo: {repo}",
    },
    'PullRequestEvent': {
        'action': "i['payload']['action']",  # opened, closed, merged, reopened, assigned, unassigned, labeled, unlabeled
        'refs': {
            'ref_type': 'PullRequest',
            'obj_no': "i['payload']['number']",
        },
        'action_str': f"{action} PullRequest: {obj_no}"
    },
    'PullRequestReviewEvent': {
        'action': "i['payload']['action']",  # created, updated, dismissed
        'refs': {
            'ref_type': 'PullRequest Review',
            'obj_no': "i['payload']['pull_request']['number']", # Used number, but not sure of nesting under PR obj
            'obj_name': "i['payload']['review']",  # Review obj affected, not sure of nesting past review
        },
        'action_str': f"{actor} {action} PR Review | PR: #{obj_no} | Repo: {repo}",
    },
    'PullRequestReviewCommentEvent': {
        'action': "i['payload']['action']",  # created
        'refs': {
            'ref_type': 'PullRequest',
            'obj_no': "i['payload']['pull_request']['number']", # Used number, but not sure of nesting under PR obj
        },
        'action_str': f"{actor} {action} comment on PR Review | PR: #{obj_no} | Repo: {repo}",
    },
    'PushEvent': {
        'action': "Pushed",
        'refs': {},
        'action_str': f"{action} Commit(s) | Repo: {repo}",
    },
    'ReleaseEvent': {
        'action': "i['payload']['action']",  # published
        'refs': {
            'ref_type': 'Release',
            'obj_name': "i['payload']['release']",  # Release obj, not sure of name or number nesting
        },
        'action_str': f"{action} Release | Repo: {repo}",
    },
    'WatchEvent': {
        'action': "i['payload']['action']",  # started
        'refs': {},
        'action_str': f"{actor} {action} watching Repo: {repo}",
    },
}