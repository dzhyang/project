namespace DzhYang.Shared.HotLoadComponent.Abstractions;

[System.AttributeUsage(AttributeTargets.Assembly, Inherited = false, AllowMultiple = false)]
public sealed class HotLoadComponentAttribute : Attribute
{
    public HotLoadComponentAttribute(string name, string description, Version version)
    {
        Name = name;
        Description = description;
        Version = version;
    }
    public string Name { get; }
    public string Description { get; }
    public Version Version { get; }
}
