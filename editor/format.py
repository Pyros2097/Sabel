class Format:
    cpp = ['.c','.h','.cpp','.hpp','.cxx','.hxx']
    csharp = ['.cs','.boo','.cobra']
    css = ['.css']
    html = ['.html','.htm']
    java = ['.java']
    javascript = ['.js']
    lua = ['.lua']
    neko = ['.neko']
    python = ['.py','.pyw']
    sql = ['.sql']
    squirrel = ['.nut']
    xml = ['.xml']
    yaml = ['.yml','.yaml']
    types = [cpp,csharp,css,html,java,javascript,lua,neko,python,sql,squirrel,xml,yaml]
    
    @staticmethod
    def get(nfile):
        for langs in Format.types:
            #print langs
            for ext in langs:
                #print ext
                if(nfile.endswith(ext)):
                    return  Format.types.index(langs)
            
        