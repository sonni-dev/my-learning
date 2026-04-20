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
        'ref_type': None,
        'obj_name': None,
        'obj_no': None,
        'target': 'comment',
        'action_str': "Commit Comment | Repo:",
    },
    'CreateEvent': {
        'action': "Created",
        'ref_type': "i['payload']['ref_type']", # branch, tag, repository
        'obj_name': None,
        'obj_no': None,
        'action_str': 'Created',
    },
    'DeleteEvent': {
        'action': "Deleted",
        'ref_type': "i['payload']['ref_type']", # branch, tag
        'obj_name': None,
        'obj_no': None,
        'action_str': 'Deleted',
    },
    'DiscussionEvent': {
        'action': "i['payload']['action']",  # created
        'ref_type': 'Discussion',
        'obj_name': "i['payload']['discussion']",
        'obj_no': None,
        'target': 'discussion',
        'action_str': "Discussion | Repo:",
    },
    'ForkEvent': {
        'action': "i['payload']['action']",  # forked
        'ref_type': 'Repository',
        'obj_name': "i['payload']['forkee']",
        'obj_no': None,
        'target': 'forkee',
        'action_str': "Repo:",
    },
    'GollumEvent': {
        'action': "Created/Updated",  # General without looping through each page
        'ref_type': 'Wiki Page(s)',
        'obj_name': None,
        'obj_no': "len(i['payload']['pages'])",
        'target': 'pages',
        'action_str': "{action} {obj_no} {ref_type} | Repo: {repo}",
    },
    'IssueCommentEvent': {
        'action': "i['payload']['action']",  # created
        'ref_type': 'Issue',
        'obj_no': "i['payload']['issue']['number']",
        'obj_name': "i['payload']['issue']['title']",
        'target': 'issue',
        'action_str': "Comment | Issue: #",
    },
    'IssuesEvent': {
        'action': "i['payload']['action']",  # closed, labeled, opened, assigned, reopened
        'ref_type': 'Issue',
        'obj_no': "i['payload']['issue']['number']",
        'obj_name': "i['payload']['issue']['title']",
            # Only present if assigned is action
            # 'assignee': "i['payload']['assignee']['login']" or "",
            # 'assignees_list': "i['payload']['assignees']" or [],
            # 'assignees': [x.login for x in assignees_list] if assignees_list else [],
            # 'no_assignees': len(assignees_list) or 0,
        'target': 'issue',
        'action_str': "| Issue: #",
    },
    'MemberEvent': {
        'action': "i['payload']['action']",  # added if user accepted invite to repo
        'ref_type': 'User',
        'obj_name': "i['payload']['member']",
        'obj_no': None,
        'target': 'member',
        'action_str': "{action} {ref_type}: {obj_name} | Repo: {repo}",
    },
    'PublicEvent': {
        'action': "Made Public",
        'ref_type': None,
        'obj_name': None,
        'obj_no': None,
        'action_str': "{action} | Repo: {repo}",
    },
    'PullRequestEvent': {
        'action': "i['payload']['action']",  # opened, closed, merged, reopened, assigned, unassigned, labeled, unlabeled
        'ref_type': 'PullRequest',
        'obj_no': "i['payload']['number']",
        'obj_name': None,
        'target': 'number',
        'action_str': "{action} PullRequest: {obj_no}"
    },
    'PullRequestReviewEvent': {
        'action': "i['payload']['action']",  # created, updated, dismissed
        'ref_type': 'PullRequest Review',
        'obj_no': "i['payload']['pull_request']['number']", # Used number, but not sure of nesting under PR obj
        'obj_name': "i['payload']['review']",  # Review obj affected, not sure of nesting past review
        'target': 'pull_request',
        'action_str': "PR Review | PR: #",
    },
    'PullRequestReviewCommentEvent': {
        'action': "i['payload']['action']",  # created
        'ref_type': 'PullRequest',
        'obj_no': "i['payload']['pull_request']['number']", # Used number, but not sure of nesting under PR obj
        'obj_name': None,
        'target': 'pull_request',
        'action_str': "Comment on PR Review | PR: #",
    },
    'PushEvent': {
        'action': "Pushed",
        'ref_type': None,
        'obj_name': None,
        'obj_no': None,
        'action_str': "{action} Commit(s) | Repo: {repo}",
    },
    'ReleaseEvent': {
        'action': "i['payload']['action']",  # published
        'ref_type': 'Release',
        'obj_name': "i['payload']['release']",  # Release obj, not sure of name or number nesting
        'obj_no': None,
        'target': 'release',
        'action_str': "Release | Repo:",
    },
    'WatchEvent': {
        'action': "i['payload']['action']",  # started
        'ref_type': None,
        'obj_name': None,
        'obj_no': None,
        'action_str': "{actor} {action} watching Repo: {repo}",
    },
}