Title: Emojibook
Date: 2021-08-15

We are presented are django app which allows us to store text notes that can contain special placeholders which will be replaced by emoji images after uploading the note. For example

    :::
    :grinning_face:

will be resolved to an image file name 1F600.png. The possible emoji keys that can be used are specified by the emoj.json file.

    :::javascript
    {
        "grinning_face": "1F600", 
        "grinning_face_with_big_eyes": "1F603",
        ...
    }

By looking at the forms.py file we can see that before a note gets saved into the database the emoji keys will already be replaced by special place holders containing the file name of the image.

    :::python
    class NoteCreateForm(forms.ModelForm):
        ...
    
        def save(self, commit=True):
            instance = super(NoteCreateForm, self).save(commit=False)
            instance.author = self.user
            instance.body = instance.body.replace("{{", "").replace("}}", "").replace("..", "")
    
            with open("emoji.json") as emoji_file:
                emojis = json.load(emoji_file)
    
                for emoji in re.findall("(:[a-z_]*?:)", instance.body):
                    instance.body = instance.body.replace(emoji, "{{" + emojis[emoji.replace(":", "")] + ".png}}")
    
            if commit:
                instance.save()
                self._save_m2m()
    
            return instance

So a note containing only the grinning_face emoji will be stored as:

    :::
    {{1F600.png}}

What we also see in the forms.py is an attempt to prevent the user from manually entering the internally used placeholders.

    :::python
    instance.body = instance.body.replace("{{", "").replace("}}", "").replace("..", "")

But this mechanism can be tricked if we would enter something like this in a note:

    :::
    {}}{/flag.txt}..}

After the replacements of {{, }} and .. happened the result still would be a note containig a placeholder in the internal format pointing to the file containing the flag:

    :::
    {{/flag.txt}}

If we open the note again in the browser we will see an image that cannot be displayed. A quick look at the views.py reveals why:

    :::python
    def view_note(request: HttpRequest, pk: int) -> HttpResponse:
        note = get_object_or_404(Note, pk=pk)
        text = note.body
        for include in re.findall("({{.*?}})", text):
            print(include)
            file_name = os.path.join("emoji", re.sub("[{}]", "", include))
            with open(file_name, "rb") as file:
                text = text.replace(include, f"<img src=\"data:image/png;base64,{base64.b64encode(file.read()).decode('latin1')}\" width=\"25\" height=\"25\" />")
    
        return render(request, "note.html", {"note": note, "text": text})

The internal placeholders are replaced with an img tag that contains the image data in base64 format - or in our case the flag. All that is left to do is to look at the source code within the web browser, find that base64 string and decode it to get the flag.

