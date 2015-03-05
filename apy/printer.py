def pr_str(mal):
  # If it's a list, map str over elements, join with spaces and surround parens
  # Otherwise just str it.
  if isinstance(mal, list):
    return'(' + ' '.join([pr_str(x) for x in mal]) + ')'
  elif isinstance(mal, tuple):
    return '[' + ' '.join([pr_str(x) for x in mal]) + ']'
  elif isinstance(mal, str):
    return ('"%s"' % mal)
  elif mal == None:
    return 'nil'
  elif isinstance(mal, bool):
    if mal == true:
      return 'true'
    else:
      return 'false'
  else:
    return repr(mal)