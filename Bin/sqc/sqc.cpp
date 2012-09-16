#include <iostream>
#include <fstream>
#include <squirrel.h>
#include <sqstdio.h>

using std::cout;

void compile_error_handler(HSQUIRRELVM v, const SQChar* desc, const SQChar* source, SQInteger line, SQInteger column)
{
    cout<<line<<","<<column<<","<<desc<< std::endl;
}

int main(int argc, char** argv)
{
    if (argc < 2) {
        cout << "Usage: " << argv[0] << " <source> <destination>" << std::endl;
        return 0;
    }

    // open vm
    HSQUIRRELVM v = sq_open(1024);
    if (!v) {
        cout << "Could not open Squirrel VM" << std::endl;
        return 0;
    }

    // set compile error handler
    sq_setcompilererrorhandler(v, compile_error_handler);

    // compile source file
    if (SQ_FAILED(sqstd_loadfile(v, argv[1], SQTrue))) {
        //cout << "Could not compile source file " << argv[1] << std::endl;
        sq_close(v);
        return 0;
    }
				
    // serialize closure containing the source
    //if (SQ_FAILED(sqstd_writeclosuretofile(v, "1.cnut"))) {
    //    cout << "Could not serialize closure" << std::endl;
    //}

    sq_close(v);
	 cout <<"Success";
    return 0;
}