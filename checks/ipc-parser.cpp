#include "CLI11.hpp"
#include <iostream>
#include <string>
#include <vector>
int main(int argc,char**argv){
 CLI::App cli;std::string path,target,name;std::vector<std::string> args;
 auto* sub=cli.add_subcommand("ipc")->require_subcommand();sub->add_option("-p",path);
 auto* show=sub->add_subcommand("show");auto* call=sub->add_subcommand("call");
 call->add_option("target",target);call->add_option("function",name);call->add_option("arguments",args)->allow_extra_args();
 CLI11_PARSE(cli,argc,argv);
 if(*show){std::cout<<"Wrong subcommand\n";return 2;}
 std::cout<<target<<"|"<<name;for(auto&a:args)std::cout<<"|"<<a;std::cout<<"\n";
}
