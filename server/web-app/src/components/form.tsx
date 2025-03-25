import React from "react"

// interface InputField {
//   name: string
//   label: string
//   type?: string
//   placeholder?: string
// }

// interface FormProps {
//   fields: InputField[]
//   onSubmit: (data: Record<string, string>) => void
// }

const Form = () => {
//   const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
//     e.preventDefault();
//     const formData = new FormData(e.currentTarget);
//     const data: Record<string, string> = {};
//     fields.forEach((field) => {
//       data[field.name] = formData.get(field.name) as string;
//     });
//     onSubmit(data);
//   };

  return (
    <div className="border-b border-gray-900/10 pb-12">
        <h2 className="text-base/7 font-semibold text-gray-900">Authentication</h2>
        <p className="mt-1 text-sm/6 text-gray-600">Please provide a valid email address where we can securely contact you.</p>
        <div className="mt-2 mb-8">
            <div className="sm:col-span-full">
                <label htmlFor="email" className="block text-sm/6 font-medium text-gray-900">
                    Email address
                </label>
                <div className="mt-2">
                    <input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    placeholder="fitness_guys@ict720.taist"
                    className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                    required
                    />
                </div>
            </div>
        </div>
    

        <h2 className="text-base/7 font-semibold text-gray-900">Personal Information</h2>
        <p className="mt-1 text-sm/6 text-gray-600">Personal details to help us personalize your experience.</p>

        <div className="mt-2 mb-8 grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6">
            <div className="sm:col-span-3">
              <label htmlFor="first-name" className="block text-sm/6 font-medium text-gray-900">
                First name
              </label>
              <div className="mt-2">
                <input
                  id="first-name"
                  name="first-name"
                  type="text"
                  autoComplete="Knat & Luca"
                  placeholder="Knat & Luca"
                  className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                  required
                />
              </div>
            </div>

            <div className="sm:col-span-3">
              <label htmlFor="last-name" className="block text-sm/6 font-medium text-gray-900">
                Last name
              </label>
              <div className="mt-2">
                <input
                  id="last-name"
                  name="last-name"
                  type="text"
                  autoComplete="Narodomy"
                  placeholder="Narodomy"
                  className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                  required
                />
              </div>
            </div>

            <div className="sm:col-span-3">
              <label htmlFor="gender" className="block text-sm/6 font-medium text-gray-900">
                Gender 
              </label>
              <div className="mt-2">
                <select
                    id="gender"
                    name="gender"
                    autoComplete="-"
                    className="col-start-1 row-start-1 w-full appearance-none rounded-md bg-white py-1.5 pr-8 pl-3 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                    defaultValue={"-"}
                    required
                >
                    <option value={"-"}>Not specified</option>
                    <option value={"male"}>Male</option>
                    <option value={"female"}>Female</option>
                </select>
                    {/* <ChevronDownIcon
                    aria-hidden="true"
                    className="pointer-events-none col-start-1 row-start-1 mr-2 size-5 self-center justify-self-end text-gray-500 sm:size-4"
                    /> */}
              </div>
            </div>


            <div className="sm:col-span-3">
              <label htmlFor="nationality" className="block text-sm/6 font-medium text-gray-900">
                Nationality 
              </label>
              <div className="mt-2">
                <input
                  id="nationality"
                  name="nationality"
                  type="text"
                  autoComplete="Thai"
                  placeholder="Thai"
                  className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                />
              </div>
            </div>




            <div className="col-span-full">
              <label htmlFor="birthday" className="block text-sm/6 font-medium text-gray-900">
                Date of birth
              </label>
              <div className="mt-2">
                <input
                  id="birthday"
                  name="birthday"
                  type="date"
                  autoComplete="birthday"
                  className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                  placeholder="Date"
                  required
                />
              </div>
            </div>


            <div className="sm:col-span-2">
              <label htmlFor="age" className="block text-sm/6 font-medium text-gray-900">
                Age
              </label>
              <div className="mt-2">
                <input
                  id="age"
                  name="age"
                  type="number"
                  autoComplete="18"
                  placeholder="18"
                  min={1}
                  className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                  required
                />
              </div>
            </div>

            <div className="sm:col-span-2">
              <label htmlFor="weight" className="block text-sm/6 font-medium text-gray-900">
                Weight
              </label>
              <div className="mt-2">
                <input
                  id="weight"
                  name="weight"
                  type="number"
                  autoComplete="50"
                  placeholder="50"
                  min={1}
                  className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                />
              </div>
            </div>

            <div className="sm:col-span-2">
              <label htmlFor="height" className="block text-sm/6 font-medium text-gray-900">
                Height
              </label>
              <div className="mt-2">
                <input
                  id="height"
                  name="height"
                  type="number"
                  autoComplete="160"
                  placeholder="160"
                  min={1}
                  className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                />
              </div>
            </div>

            <div className="sm:col-span-4">
              <label htmlFor="phone-number" className="block text-sm/6 font-medium text-gray-900">
                Phone Number	
              </label>
              <div className="mt-2">
                <input
                  id="phone-number"
                  name="phone-number"
                  type="tel"
                  pattern="[0-9]{3}-[0-9]{2}-[0-9]{3}"
                  autoComplete="123-45-678"
                  placeholder="123-45-678"
                  className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                />
              </div>
            </div>

        </div>

        <h2 className="mt-8 text-base/7 font-semibold text-gray-900">Occupation Details</h2>
        <p className="mt-1 text-sm/6 text-gray-600">Provide information about your current occupation.</p>

        <div className="mt-2 mb-8 grid grid-cols-1 gap-x-6 gap-y-4 sm:grid-cols-6">
        <div className="sm:col-span-3">
              <label htmlFor="company-name" className="block text-sm/6 font-medium text-gray-900">
                Company Name 
              </label>
              <div className="mt-2">
                <input
                  id="company-name"
                  name="company-name"
                  type="text"
                  autoComplete="ICT720"
                  placeholder="ICT720"
                  className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                />
              </div>
            </div>

            <div className="sm:col-span-3">
              <label htmlFor="job" className="block text-sm/6 font-medium text-gray-900">
                Job
              </label>
              <div className="mt-2">
                <input
                  id="job"
                  name="job"
                  type="text"
                  autoComplete="Student"
                  placeholder="Student"
                  className="block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6"
                />
              </div>
            </div>
        </div>
    </div>

    // <form onSubmit={handleSubmit} className="bg-white shadow-lg rounded-lg p-6 space-y-4 w-full max-w-md mx-auto">
    //   <h2 className="text-2xl font-semibold text-gray-700 text-center">Fill the Form</h2>
      
    //   {fields.map((field) => (
    //     <div key={field.name} className="flex flex-col">
    //       <label className="text-gray-600 font-medium mb-1">{field.label}</label>
    //       <input
    //         type={field.type || "text"}
    //         name={field.name}
    //         placeholder={field.placeholder || ""}
    //         className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
    //       />
    //     </div>
    //   ))}

    //   <button 
    //     type="submit" 
    //     className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition duration-200"
    //   >
    //     Submit
    //   </button>
    // </form>
  );
}

export default Form