using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks; 

namespace ConsoleApp1
{
    /// <summary>
    /// Alternativa ao uso de estruturas enum para representar conjuntos de tipos ou estados.
    /// Outra opção é usar o pacote NuGet Ardalis.SmartEnum
    /// </summary>
    public class JobTitle
    {
        // this must appear before other static instance types.
        public static List<JobTitle> AllTitles { get; } = new List<JobTitle>();

        public static JobTitle Author { get; } = new JobTitle(0, "Author");
        public static JobTitle Editor { get; } = new JobTitle(1, "Editor");
        public static JobTitle Administrator { get; } = new JobTitle(2, "Administrator");
        public static JobTitle SalesRep { get; } = new JobTitle(3, "Sales Representative");

        public string Name { get; private set; }
        public int Value { get; private set; }

        private JobTitle(int val, string name)
        {
            Value = val;
            Name = name;
            AllTitles.Add(this);
        }

        public static JobTitle FromString(string jobTitleMemberName)
        {
             return AllTitles.Single(r => String.Equals(r.Name, jobTitleMemberName, StringComparison.OrdinalIgnoreCase));
        }

        public static JobTitle FromValue(int value)
        {
            return AllTitles.Single(r => r.Value == value);
        }

        public override bool Equals(System.Object obj)
        {
            // If parameter is null return false.
            JobTitle other = obj as JobTitle;
            if (other == null) { return false; }

            return Equals(other);
        }

        public bool Equals(JobTitle other)
        {
            if ((object)other == null) { return false; }

            // Return true if the values match:
            return (Value == other.Value);
        }

        public override int GetHashCode()
        {
            return Value;
        }

        public static bool operator ==(JobTitle a, JobTitle b)
        {
            // If both are null, or both are same instance, return true.
            if (System.Object.ReferenceEquals(a, b)) { return true; }
            // If one is null, but not both, return false.
            if ((object)a == null || (object)b == null) { return false; }

            // Return true if Equal match:
            return a.Equals(b);
        }

        public static bool operator !=(JobTitle a, JobTitle b)
        {
            return !(a == b);
        }
    }
}
