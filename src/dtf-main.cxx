#include "lwtnn/LightweightGraph.hh"
#include "lwtnn/parse_json.hh"

#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <cmath>

typedef std::map<std::string, std::map<std::string, double> > input_t;

input_t dummy_feature_map() {
  return {
    {"inputs", {
        {"jet_pt_log1p", std::log1p(1)},
        {"jet_m_log1p", std::log1p(1)},
        {"jet_eta", 1},
        {"jet_phi", 1},
        {"photon_E_log1p", std::log1p(1)},
        {"photon_pt_log1p", std::log1p(1)},
        {"photon_eta", 1},
        {"photon_phi", 1},
        {"jet_tau21", 1},
        {"jet_D2", 1} }
    }
  };
}

int main(int argc, char* argv[]) {
  using namespace lwt;
  std::ifstream input("data/lwtnn-dtf-config.json");;
  LightweightGraph graph(parse_json_graph(input));
  auto outmap = graph.compute(dummy_feature_map());
  std::cout << outmap.at("discriminant") << std::endl;
  return 0;
}
