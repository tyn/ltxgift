import sys
import re
import cgi

def escape_gift(s):
  s = cgi.escape(s)
  s = s.replace('\\', r'\\')
  s = re.sub('~', '\~', s)
  s = re.sub('=', '\=', s)
  s = re.sub('#', '\#', s)
  s = re.sub('{', '\{', s)
  s = re.sub('}', '\}', s)
  s = re.sub(':', '\:', s)
  return s

def to_gift(data):
  out=[]
  out.append("$CATEGORY: %s " % data['category'])
  out.append("")
  for prob in data['problems']:
    out.append("")
    if 'qtitle' in prob:
      qtitle = escape_gift(prob['qtitle'])
    else:
      qtitle = escape_gift(prob['question'])
    out.append("::%s::[html]<div style\='display\:none;'>%s</div>%s{" % (qtitle, escape_gift('\(\let\gdef\def' + data['common'] + '\)'), escape_gift(prob['question'])))
    for it in prob['items']:
      symbol = '?'
      if it['type'] == 'correct':
        symbol = '='
      elif it['type'] == 'wrong':
        symbol = '~'
      else:
        raise ("Unknown type: %s" % it['type'])
      response = ""
      if it.has_key("response"):
        response = "# %s" % it['response']
      out.append("\t%s %s %s" % (symbol, escape_gift("\n".join(it['text'])), response))
    out.append("}")
  return "\n".join(out)

def main():
  with open(sys.argv[1]) as f:
    data = {'category':'no-category', 'problems':[], 'common':''}
    current_tag = None
    current_text = []
    target = data
    lines = f.readlines()
    for line in lines:
      line = re.sub(r'[\r\n]+$', '', line)
      m = re.search('<(/?)([-a-zA-Z0-9]+)>', line)
      if m:
        if m.group(1) == '/':
          is_begin = 0
        else:
          is_begin = 1
        tag = m.group(2)
        if is_begin: # end tag
          current_tag = tag
          if 'problem' == current_tag:
            target = {'items':[]}
            data['problems'].append(target)
          else:
            pass
        else:
          text = "   ".join(current_text)
          if re.match(r'^(category)$', tag):
            data['category'] = text
          elif re.match(r'^(qtitle)$', tag):
            target[tag] = target.get(tag, "") + text
          elif re.match(r'^(question)$', tag):
            target[tag] = target.get(tag, "") + text
          elif re.match(r'^(correct|wrong)$', tag):
            target['last_item'] = {'type':tag, 'text':current_text};
            target['items'].append(target['last_item']);
          elif re.match(r'^(response)$', tag):
            target['last_item']['response'] = text;
          elif re.match(r'^(common)$', tag):
            data['common'] = data.get('common', "") + text
          current_text = []
      else:
        current_text.append(line)
    print to_gift(data)

if __name__ == "__main__":
	main()
