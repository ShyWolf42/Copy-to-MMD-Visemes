# Copy to MMD Visemes

This blender add-on was created to easily create copies of viseme shapekeys with the japanese names that MMD animations
would expect. It is primarily aimed at use for VRChat MMD Worlds to enable your avatar to lipsync and do facial
expressions to the songs.

After installing the add-on the "MMD Shapekeys" interface will show up in the `Object Data properties` tab (where the
shapekeys are listed as well)

![Screenshot of the UI](/images/MMDShapekeys.jpg)

* **[x] Fill Existing Target Shape Keys As Placeholder**: if the correct japanese shape key name already exists on the model,
  set that as the value. This key will not be duplicated, the primary purpose is to show that this Viseme / shapekey is already set up.
* **[Import from / Export to Clipboard]**: Saves / loads the values as JSON for easier sharing. If a configuration references a shape key
  that does not exist on the model it will be ignored.
* **[Prefill Values]** Fill in the existing shapekeys based on their names. Visemes can have a prefix, for the
  other shapekeys like _blink_ the names must match. Values that have already been set will not be overwritten.
* **[Duplicate Shape Keys With MMD Names]** will clone the shapekeys set in the list and give them their Japanese MMD names.
  An empty shapekey will be added below the Visemes, and above the other shapekeys to have them grouped.

![generated MMD shapekeys](/images/MMDShapekeys_result.jpg)