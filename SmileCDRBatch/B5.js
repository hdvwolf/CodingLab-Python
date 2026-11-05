import * as json from 'json';
import * as requests from 'requests';
import * as schedule from 'schedule';
import * as time from 'time';

var _pj;

function _pj_snippets(container) {
  function in_es6(left, right) {
    if (right instanceof Array || typeof right === "string") {
      return right.indexOf(left) > -1;
    } else {
      if (right instanceof Map || right instanceof Set || right instanceof WeakMap || right instanceof WeakSet) {
        return right.has(left);
      } else {
        return left in right;
      }
    }
  }

  container["in_es6"] = in_es6;
  return container;
}

_pj = {};

_pj_snippets(_pj);

function BatchLoad() {
  var CBaseURL, Cdata, ClaimsFilePath, ControlFilePath, EBaseURL, Edata, EnconterFilePath, LogFilePath, PBaseURL, PatientData, PatientFilePath, Pdata, aindent, bindent, control_file, cref, data, e, encounterlist, encounters, eref, eurl, f, headers, http, itemlist, itemlistvalue, jo, json_object, l, last_line_read, linestoload, lp, matchstring, matchstring1, output, plist, pref, purl, s, z;
  PatientFilePath = "/Downloads/SmileCDRBatch/Patient.ndjson";
  EnconterFilePath = "/Downloads/SmileCDRBatch/EncounterSorted.ndjson";
  ClaimsFilePath = "/Downloads/SmileCDRBatch/Claim.ndjson";
  LogFilePath = "/Users/kishorekulkarni/Downloads/SmileCDRBatch/log.txt";
  ControlFilePath = "/Users/kishorekulkarni/Downloads/SmileCDRBatch/ctrl.json";
  PBaseURL = "http://localhost:8000/Patient";
  EBaseURL = "http://localhost:8000/Encounter";
  CBaseURL = "http://localhost:8000/Claim";
  headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
  };
  plist = [];
  linestoload = 15000;
  control_file = open(ControlFilePath, "r");
  json_object = json.load(control_file);
  control_file.close();
  last_line_read = json_object["linecounter"];
  Pdata = open(PatientFilePath, "r", {
    "encoding": "latin-1"
  }).readlines();
  PatientData = Pdata.slice(last_line_read, last_line_read + linestoload);

  for (var x, _pj_c = 0, _pj_a = PatientData, _pj_b = _pj_a.length; _pj_c < _pj_b; _pj_c += 1) {
    x = _pj_a[_pj_c];
    headers = {
      "Accept": "application/json",
      "Content_Type": "application/json"
    };
    data = x.encode("utf-8", "ignore").decode("utf-8", "replace");
    s = requests.session();
    s.headers = headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
    };
    http = s.post(PBaseURL, data);
    f = open(LogFilePath, "a");
    output = json.dumps(http.json());
    f.write(output);
    f.close();
    lp = open("tmp.txt", "w");
    lp.write(x);
    lp.close();
    l = open("tmp.txt", "r");
    jo = json.load(l);
    l.close();
    pref = jo["id"];
    plist.append(pref);
  }

  json_object["linecounter"] = last_line_read + linestoload;
  control_file = open(ControlFilePath, "w");
  json.dump(json_object, control_file);
  control_file.close();
  Edata = open(EnconterFilePath, "r", {
    "encoding": "latin-1"
  }).readlines();

  for (var x, _pj_c = 0, _pj_a = Edata, _pj_b = _pj_a.length; _pj_c < _pj_b; _pj_c += 1) {
    x = _pj_a[_pj_c];
    headers = {
      "Accept": "application/json",
      "Content_Type": "application/json"
    };
    data = x.encode("utf-8", "ignore").decode("utf-8", "replace");
    lp = open("tmp.txt", "w");
    lp.write(x);
    lp.close();
    l = open("tmp.txt", "r");
    jo = json.load(l);
    l.close();
    eref = jo["id"];
    pref = jo["subject"]["reference"];
    matchstring = pref.strip("Patient/");

    if (_pj.in_es6(matchstring, plist)) {
      s = requests.session();
      s.headers = headers;
      http = s.post(EBaseURL, data);
      f = open(LogFilePath, "a");
      output = json.dumps(http.json());
      f.write(output);
      f.close();
    }
  }

  Cdata = open(ClaimsFilePath, "r", {
    "encoding": "latin-1"
  }).readlines();

  for (var x, _pj_c = 0, _pj_a = Cdata, _pj_b = _pj_a.length; _pj_c < _pj_b; _pj_c += 1) {
    x = _pj_a[_pj_c];
    headers = {
      "Accept": "application/json",
      "Content_Type": "application/json"
    };
    data = x.encode("utf-8", "ignore").decode("utf-8", "replace");
    lp = open("tmp.txt", "w");
    lp.write(x);
    lp.close();
    l = open("tmp.txt", "r");
    jo = json.load(l);
    l.close();
    cref = jo["id"];
    pref = jo["patient"]["reference"];
    e = [];
    itemlistvalue = [];
    itemlist = [];
    aindent = 0;
    bindent = 0;

    for (var y, _pj_f = 0, _pj_d = jo["item"], _pj_e = _pj_d.length; _pj_f < _pj_e; _pj_f += 1) {
      y = _pj_d[_pj_f];
      itemlist.append(jo["item"][aindent]);
      aindent = aindent + 1;
    }

    for (var y, _pj_f = 0, _pj_d = itemlist, _pj_e = _pj_d.length; _pj_f < _pj_e; _pj_f += 1) {
      y = _pj_d[_pj_f];
      itemlistvalue = itemlist[bindent];
      bindent = bindent + 1;

      if (_pj.in_es6("encounter", itemlistvalue)) {
        encounterlist = itemlistvalue["encounter"];
        z = 0;

        for (var w, _pj_i = 0, _pj_g = encounterlist, _pj_h = _pj_g.length; _pj_i < _pj_h; _pj_i += 1) {
          w = _pj_g[_pj_i];
          encounters = encounterlist[z];
          z = z + 1;
          eref = encounters["reference"];
          matchstring = pref.strip("Patient/");
          matchstring1 = eref.strip("Encounter/");
          purl = PBaseURL + "?identifier=" + matchstring;
          eurl = EBaseURL + "?identifier=" + matchstring1;

          if (requests.get(purl).status_code === 200) {
            if (requests.get(eurl).status_code === 200) {
              s = requests.session();
              s.headers = headers;
              http = s.post("http://localhost:8000/Claim", data);
              f = open(LogFilePath, "a");
              output = json.dumps(http.json());
              f.write(output);
              f.close();
            }
          }
        }
      } else {
        matchstring = pref.strip("Patient/");
        purl = "http://localhost:8000/Patient" + matchstring;

        if (requests.get(purl).status_code === 200) {
          s = requests.session();
          s.headers = headers;
          http = s.post(CBaseURL, data);
          f = open(LogFilePath, "a");
          output = json.dumps(http.json());
          f.write(output);
          f.close();
        }
      }
    }
  }
}

while (true) {
  schedule.run_pending();
  time.sleep(0);
}
